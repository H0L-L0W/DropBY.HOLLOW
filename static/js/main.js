// DropBy.HOLLOW - Main JavaScript

// Utility functions
const Utils = {
    // Format price to currency
    formatPrice: (price) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(price);
    },
    
    // Show notification
    showNotification: (message, type = 'info') => {
        console.log(`[${type.toUpperCase()}] ${message}`);
    },
    
    // Fetch API wrapper
    async fetch(url, options = {}) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('Fetch error:', error);
            throw error;
        }
    }
};

// Cart functionality
const Cart = {
    items: [],
    
    // Initialize cart from session storage
    init: () => {
        const stored = sessionStorage.getItem('cart');
        if (stored) {
            Cart.items = JSON.parse(stored);
        }
    },
    
    // Add item to cart
    add: (product) => {
        const existing = Cart.items.find(item => item.id === product.id);
        if (existing) {
            existing.quantity += 1;
        } else {
            Cart.items.push({ ...product, quantity: 1 });
        }
        Cart.save();
        Cart.updateUI();
    },
    
    // Remove item from cart
    remove: (productId) => {
        Cart.items = Cart.items.filter(item => item.id !== productId);
        Cart.save();
        Cart.updateUI();
    },
    
    // Update item quantity
    updateQuantity: (productId, quantity) => {
        const item = Cart.items.find(item => item.id === productId);
        if (item) {
            item.quantity = Math.max(1, quantity);
            Cart.save();
            Cart.updateUI();
        }
    },
    
    // Get cart total
    getTotal: () => {
        return Cart.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    },
    
    // Save to storage
    save: () => {
        sessionStorage.setItem('cart', JSON.stringify(Cart.items));
    },
    
    // Update UI elements
    updateUI: () => {
        const cartCount = document.querySelector('.cart-count');
        if (cartCount) {
            const count = Cart.items.reduce((sum, item) => sum + item.quantity, 0);
            cartCount.textContent = count;
        }
    },
    
    // Clear cart
    clear: () => {
        Cart.items = [];
        Cart.save();
        Cart.updateUI();
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    Cart.init();
    Cart.updateUI();
});

// API functions for frontend
const API = {
    baseUrl: '/api',
    
    // Categories
    getCategories: () => Utils.fetch(`${API.baseUrl}/categories`),
    getCategory: (id) => Utils.fetch(`${API.baseUrl}/categories/${id}`),
    
    // Products
    getProducts: (params = {}) => {
        const query = new URLSearchParams(params).toString();
        return Utils.fetch(`${API.baseUrl}/products?${query}`);
    },
    getProduct: (id) => Utils.fetch(`${API.baseUrl}/products/${id}`),
    scrapeProduct: (id) => Utils.fetch(`${API.baseUrl}/products/${id}/scrape`, { method: 'POST' }),
    
    // Orders
    createOrder: (data) => Utils.fetch(`${API.baseUrl}/orders`, {
        method: 'POST',
        body: JSON.stringify(data)
    }),
    getOrder: (id) => Utils.fetch(`${API.baseUrl}/orders/${id}`),
    updateOrderStatus: (id, status) => Utils.fetch(`${API.baseUrl}/orders/${id}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status })
    }),
    
    // Payment
    createPaymentIntent: (amount) => Utils.fetch(`${API.baseUrl}/payment/create-intent`, {
        method: 'POST',
        body: JSON.stringify({ amount })
    })
};

// Export for use in other scripts
window.DropBy = {
    Utils,
    Cart,
    API
};
</parameter>
</invoke>
</minimax:tool_call>
