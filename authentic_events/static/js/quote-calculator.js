// Quote Calculator for Authentic Events
class QuoteCalculator {
    constructor() {
        this.init();
    }

    init() {
        // Configuration
        this.config = {
            basePrices: {
                wedding: { basic: 50000, standard: 80000, premium: 150000 },
                corporate: { basic: 30000, standard: 50000, premium: 100000 },
                birthday: { basic: 20000, standard: 35000, premium: 60000 },
                festival: { basic: 15000, standard: 25000, premium: 40000 },
                home: { basic: 10000, standard: 20000, premium: 35000 }
            },
            cityMultipliers: {
                metro: 1.5,
                tier2: 1.2,
                tier3: 1.0,
                local: 0.7
            },
            materialMultipliers: {
                economy: 0.7,
                standard: 1.0,
                premium: 1.5
            },
            materialDescriptions: {
                economy: 'Budget-friendly materials, decent quality',
                standard: 'Good quality materials, beautiful designs',
                premium: 'Imported/High-end materials, intricate designs'
            }
        };

        // Initialize event listeners
        this.setupEventListeners();
        this.setupCityAutoDetect();
        this.initializeForm();
    }

    setupEventListeners() {
        // Calculate button
        $(document).on('click', '#calculateQuote', () => this.calculateQuote());

        // Real-time calculation on input change
        $(document).on('change', '.quote-input', () => this.calculateQuote());

        // City type auto-detection
        $(document).on('blur', '#cityInput', () => this.detectCityType());

        // Package selection
        $(document).on('change', 'input[name="packageLevel"]', () => this.calculateQuote());

        // Material grade selection
        $(document).on('change', 'input[name="materialGrade"]', () => this.calculateQuote());

        // Event type selection
        $(document).on('change', '#eventType', () => this.updateEventDetails());

        // Guest count slider
        $(document).on('input', '#guestCount', function() {
            $('#guestCountValue').text($(this).val());
            this.calculateQuote();
        }.bind(this));

        // Venue size slider
        $(document).on('input', '#venueSize', function() {
            $('#venueSizeValue').text($(this).val() + ' sq.ft.');
            this.calculateQuote();
        }.bind(this));
    }

    setupCityAutoDetect() {
        // City database
        this.cityDatabase = {
            metro: [
                'mumbai', 'delhi', 'bangalore', 'hyderabad', 'chennai',
                'kolkata', 'pune', 'ahmedabad', 'surat', 'jaipur'
            ],
            tier2: [
                'lucknow', 'kanpur', 'nagpur', 'indore', 'thane',
                'bhopal', 'visakhapatnam', 'patna', 'vadodara', 'coimbatore'
            ],
            tier3: [
                'ghaziabad', 'ludhiana', 'agra', 'nashik', 'faridabad',
                'meerut', 'rajkot', 'varanasi', 'srinagar', 'jodhpur'
            ]
        };
    }

    initializeForm() {
        // Set default values
        $('#guestCountValue').text($('#guestCount').val());
        $('#venueSizeValue').text($('#venueSize').val() + ' sq.ft.');

        // Set today as min date
        const today = new Date().toISOString().split('T')[0];
        $('#eventDate').attr('min', today);

        // Calculate initial quote
        this.calculateQuote();
    }

    detectCityType() {
        const cityInput = $('#cityInput').val().trim().toLowerCase();
        if (!cityInput) return;

        let cityType = 'local';
        let cityTypeName = 'Local City';

        // Check metro cities
        if (this.cityDatabase.metro.includes(cityInput)) {
            cityType = 'metro';
            cityTypeName = 'Metro City';
        }
        // Check tier2 cities
        else if (this.cityDatabase.tier2.includes(cityInput)) {
            cityType = 'tier2';
            cityTypeName = 'Tier 2 City';
        }
        // Check tier3 cities
        else if (this.cityDatabase.tier3.includes(cityInput)) {
            cityType = 'tier3';
            cityTypeName = 'Tier 3 City';
        }

        // Update hidden field
        $('#cityType').val(cityType);

        // Show city type info
        this.showCityTypeInfo(cityTypeName, cityType);

        // Recalculate quote
        this.calculateQuote();
    }

    showCityTypeInfo(cityTypeName, cityType) {
        let message = '';
        let priceRange = '';

        switch(cityType) {
            case 'metro':
                message = 'Premium materials and maximum coverage';
                priceRange = '₹75,000 - ₹2,00,000+';
                break;
            case 'tier2':
                message = 'Good quality materials and ample coverage';
                priceRange = '₹55,000 - ₹1,50,000';
                break;
            case 'tier3':
                message = 'Quality local materials and good coverage';
                priceRange = '₹35,000 - ₹1,00,000';
                break;
            default:
                message = 'Budget-friendly materials and sufficient coverage';
                priceRange = '₹25,000 - ₹75,000';
        }

        // Remove existing info if any
        $('#cityTypeInfo').remove();

        // Add new info
        $('#cityInput').after(`
            <div id="cityTypeInfo" class="alert alert-info mt-2 small animate__animated animate__fadeIn">
                <i class="fas fa-info-circle me-2"></i>
                <strong>${cityTypeName}</strong> - ${message}. Estimated range: ${priceRange}
            </div>
        `);
    }

    updateEventDetails() {
        const eventType = $('#eventType').val();
        let defaultPackage = 'standard';
        let defaultMaterial = 'standard';

        // Set defaults based on event type
        switch(eventType) {
            case 'wedding':
            case 'reception':
                defaultPackage = 'premium';
                defaultMaterial = 'premium';
                break;
            case 'corporate':
                defaultPackage = 'standard';
                defaultMaterial = 'standard';
                break;
            case 'birthday':
            case 'festival':
                defaultPackage = 'basic';
                defaultMaterial = 'economy';
                break;
        }

        // Update selections
        $(`input[name="packageLevel"][value="${defaultPackage}"]`).prop('checked', true);
        $(`input[name="materialGrade"][value="${defaultMaterial}"]`).prop('checked', true);

        // Recalculate
        this.calculateQuote();
    }

    calculateQuote() {
        // Get form values
        const eventType = $('#eventType').val() || 'wedding';
        const cityType = $('#cityType').val() || 'local';
        const packageLevel = $('input[name="packageLevel"]:checked').val() || 'standard';
        const materialGrade = $('input[name="materialGrade"]:checked').val() || 'standard';
        const guestCount = parseInt($('#guestCount').val()) || 100;
        const venueSize = parseInt($('#venueSize').val()) || 1000;

        // Validate inputs
        if (!eventType) {
            this.showError('Please select event type');
            return;
        }

        // Calculate base price
        const basePrice = this.config.basePrices[eventType] ?
            this.config.basePrices[eventType][packageLevel] : 50000;

        // Apply multipliers
        const cityMultiplier = this.config.cityMultipliers[cityType] || 1.0;
        const materialMultiplier = this.config.materialMultipliers[materialGrade] || 1.0;

        // Calculate size multipliers
        const sizeMultiplier = this.calculateSizeMultiplier(guestCount, venueSize);

        // Final calculation
        let estimatedPrice = basePrice * cityMultiplier * materialMultiplier * sizeMultiplier;

        // Round to nearest 1000
        estimatedPrice = Math.round(estimatedPrice / 1000) * 1000;

        // Format with commas
        const formattedPrice = '₹' + estimatedPrice.toLocaleString('en-IN');

        // Get description
        const materialDescription = this.config.materialDescriptions[materialGrade];

        // Update UI
        this.displayResult(formattedPrice, estimatedPrice, materialDescription, {
            eventType,
            cityType,
            packageLevel,
            materialGrade,
            guestCount,
            venueSize
        });
    }

    calculateSizeMultiplier(guestCount, venueSize) {
        let multiplier = 1.0;

        // Adjust based on guest count
        if (guestCount > 300) multiplier *= 1.3;
        else if (guestCount > 200) multiplier *= 1.2;
        else if (guestCount > 100) multiplier *= 1.1;
        else if (guestCount < 50) multiplier *= 0.9;

        // Adjust based on venue size
        if (venueSize > 2000) multiplier *= 1.2;
        else if (venueSize > 1000) multiplier *= 1.1;
        else if (venueSize < 500) multiplier *= 0.9;

        return multiplier;
    }

    displayResult(formattedPrice, estimatedPrice, materialDescription, details) {
        // Update result display
        $('#estimatedPrice').text(formattedPrice);
        $('#materialDescription').text(materialDescription);
        $('#quoteResult').removeClass('d-none').addClass('animate__animated animate__fadeIn');

        // Update breakdown
        this.updatePriceBreakdown(estimatedPrice, details);

        // Show share buttons
        this.showShareButtons(formattedPrice, details);

        // Scroll to result if not visible
        if (!this.isElementInViewport('#quoteResult')) {
            $('html, body').animate({
                scrollTop: $('#quoteResult').offset().top - 100
            }, 1000);
        }
    }

    updatePriceBreakdown(estimatedPrice, details) {
        const breakdown = `
            <div class="row">
                <div class="col-6">
                    <small class="text-muted">Event Type:</small>
                    <p class="mb-0">${this.formatEventType(details.eventType)}</p>
                </div>
                <div class="col-6">
                    <small class="text-muted">City Type:</small>
                    <p class="mb-0">${this.formatCityType(details.cityType)}</p>
                </div>
                <div class="col-6">
                    <small class="text-muted">Package:</small>
                    <p class="mb-0">${details.packageLevel.charAt(0).toUpperCase() + details.packageLevel.slice(1)}</p>
                </div>
                <div class="col-6">
                    <small class="text-muted">Material:</small>
                    <p class="mb-0">${details.materialGrade.charAt(0).toUpperCase() + details.materialGrade.slice(1)}</p>
                </div>
                <div class="col-6">
                    <small class="text-muted">Guests:</small>
                    <p class="mb-0">${details.guestCount} people</p>
                </div>
                <div class="col-6">
                    <small class="text-muted">Venue Size:</small>
                    <p class="mb-0">${details.venueSize} sq.ft.</p>
                </div>
            </div>
        `;

        $('#priceBreakdown').html(breakdown);
    }

    showShareButtons(formattedPrice, details) {
        const shareText = `I just got an estimated quote of ${formattedPrice} for ${this.formatEventType(details.eventType)} decoration from Authentic Events!`;
        const shareUrl = window.location.href;

        $('#shareWhatsApp').attr('href',
            `https://wa.me/?text=${encodeURIComponent(shareText + ' ' + shareUrl)}`
        );

        $('#shareEmail').attr('href',
            `mailto:?subject=Event Decoration Quote&body=${encodeURIComponent(shareText + '\n\n' + shareUrl)}`
        );
    }

    formatEventType(eventType) {
        const eventNames = {
            'wedding': 'Wedding',
            'reception': 'Wedding Reception',
            'engagement': 'Engagement',
            'birthday': 'Birthday Party',
            'corporate': 'Corporate Event',
            'festival': 'Festival Celebration',
            'home': 'Home Party',
            'other': 'Other Event'
        };
        return eventNames[eventType] || eventType;
    }

    formatCityType(cityType) {
        const cityNames = {
            'metro': 'Metro City',
            'tier2': 'Tier 2 City',
            'tier3': 'Tier 3 City',
            'local': 'Local City'
        };
        return cityNames[cityType] || cityType;
    }

    showError(message) {
        // Remove existing alerts
        $('.alert-danger').remove();

        // Show error
        $('#calculateQuote').before(`
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <i class="fas fa-exclamation-circle me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `);
    }

    isElementInViewport(el) {
        const rect = $(el)[0].getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    // API integration for saving quotes
    saveQuote(quoteData) {
        return $.ajax({
            url: '/api/save_quote',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(quoteData)
        });
    }

    // Export quote as PDF (placeholder)
    exportQuote() {
        alert('Export feature coming soon!');
    }
}

// Initialize when document is ready
$(document).ready(function() {
    window.quoteCalculator = new QuoteCalculator();
});

// Utility functions
function formatIndianCurrency(amount) {
    return '₹' + amount.toLocaleString('en-IN');
}

function getCitySuggestions(query) {
    const cities = [
        'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai',
        'Kolkata', 'Pune', 'Ahmedabad', 'Surat', 'Jaipur',
        'Lucknow', 'Kanpur', 'Nagpur', 'Indore', 'Thane'
    ];

    return cities.filter(city =>
        city.toLowerCase().includes(query.toLowerCase())
    );
}

// Autocomplete for city input
$(document).on('input', '#cityInput', function() {
    const query = $(this).val();
    if (query.length > 2) {
        const suggestions = getCitySuggestions(query);
        if (suggestions.length > 0) {
            // Implement autocomplete UI
            console.log('Suggestions:', suggestions);
        }
    }
});