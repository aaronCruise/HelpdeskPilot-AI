''' 
Given ticket text, determine category and priority.

This is the baseline, rule-based classification 
to compare against the AI classification.
'''

from app.models.ticket import CATEGORIES, PRIORITIES

CLASSIFICATION_RULES = {
    CATEGORIES.BILLING: {
        'keywords': ['invoice', 'refund', 'charge', 'payment', 'billing', 'price', 'subscription'],
        'priority': PRIORITIES.MEDIUM
    },
    CATEGORIES.TECHNICAL: {
        'keywords': ['error', 'bug', 'crash', 'slow', 'performance', 'issue', 'fail', 'break'],
        'priority': PRIORITIES.HIGH
    },
    CATEGORIES.HARDWARE: {
        'keywords': ['projector', 'hdmi', 'camera', 'laptop', 'monitor', 'keyboard', 'mouse', 'device', 'screen'],
        'priority': PRIORITIES.MEDIUM
    },
    CATEGORIES.SOFTWARE: {
        'keywords': ['app', 'software', 'install', 'update', 'compatibility', 'library', 'package'],
        'priority': PRIORITIES.MEDIUM
    },
    CATEGORIES.ACCOUNT: {
        'keywords': ['password', 'login', 'account', 'access', 'reset', 'auth', 'username'],
        'priority': PRIORITIES.HIGH
    },
    CATEGORIES.NETWORK: {
        'keywords': ['wifi', 'internet', 'connection', 'network', 'bandwidth', 'connectivity', 'wifi'],
        'priority': PRIORITIES.HIGH
    },
    CATEGORIES.CLASSROOM: {
        'keywords': ['classroom', 'presentation', 'class', 'projector', 'hdmi'],
        'priority': PRIORITIES.HIGH
    },
    CATEGORIES.CHECKOUT: {
        'keywords': ['checkout', 'borrow', 'return', 'loan', 'equipment', 'reserve'],
        'priority': PRIORITIES.LOW
    }
}

def classify_ticket(ticket_text: str) -> dict:
    text_lower = ticket_text.lower()
    
    # Find first matching category
    for category, rules in CLASSIFICATION_RULES.items():
        if any(keyword in text_lower for keyword in rules['keywords']):
            return {
                'category': category,
                'priority': rules['priority']
            }
    
    # Default to general if no match
    return {
        'category': CATEGORIES.GENERAL,
        'priority': PRIORITIES.MEDIUM
    }