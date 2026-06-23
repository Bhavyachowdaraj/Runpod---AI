"""
Browser Use Dataset Generator

This script helps generate a larger dataset for fine-tuning browser use models.
You can expand this with more templates and scenarios.
"""

import json
import random
from typing import List, Dict

# Action templates for browser automation
ACTIONS = {
    "click": "Action: click('{element}')",
    "type": "Action: type('{text}')",
    "press": "Action: press('{key}')",
    "hover": "Action: hover('{element}')",
    "scrollTo": "Action: scrollTo('{position}')",
    "wait": "Action: wait({seconds})",
    "read": "Action: read('{element}')",
    "verify": "Action: verify('{condition}')",
    "select": "Action: select('{value}')",
    "fill_form": "Action: fill_form({fields})",
}

# Common elements on web pages
ELEMENTS = {
    "search": ["search_box", "search_bar", "search_input", "search_button"],
    "navigation": ["menu", "nav_link", "home_button", "back_button"],
    "forms": ["submit_button", "input_field", "dropdown", "checkbox", "radio_button"],
    "content": ["article", "paragraph", "image", "video", "link"],
    "e-commerce": ["add_to_cart", "buy_now", "price_tag", "product_card", "checkout_button"],
}

# Task templates
TASK_TEMPLATES = [
    "Navigate to {website} and {action}",
    "Search for {query} on {website}",
    "Fill out the {form_type} form",
    "Click on the {element} to {purpose}",
    "Complete the {workflow} process",
]

def generate_dataset_entry() -> Dict:
    """Generate a single dataset entry for browser use."""

    scenarios = [
        # Search scenarios
        {
            "instruction": "You are a browser automation agent. Given a web task, output the sequence of actions to complete it.",
            "input": f"Task: Search for product information\nCurrent page: google.com\nAvailable elements: search_bar, search_button, result_links, images_tab, videos_tab",
            "output": "\n".join([
                ACTIONS["click"].format(element="search_bar"),
                ACTIONS["type"].format(text="product specifications"),
                ACTIONS["press"].format(key="Enter"),
                ACTIONS["wait"].format(seconds=2),
                ACTIONS["scrollTo"].format(position="middle"),
                ACTIONS["click"].format(element="result_1"),
                ACTIONS["wait"].format(seconds=1),
                ACTIONS["read"].format(element="product_details"),
            ])
        },

        # Form filling scenarios
        {
            "instruction": "You are a browser automation agent. Given a web task, output the sequence of actions to complete it.",
            "input": f"Task: Complete registration form\nCurrent page: signup\nAvailable elements: username_field, email_field, password_field, confirm_password, submit_button",
            "output": "\n".join([
                ACTIONS["click"].format(element="username_field"),
                ACTIONS["type"].format(text="newuser123"),
                ACTIONS["click"].format(element="email_field"),
                ACTIONS["type"].format(text="user@example.com"),
                ACTIONS["click"].format(element="password_field"),
                ACTIONS["type"].format(text="SecurePass!23"),
                ACTIONS["click"].format(element="confirm_password"),
                ACTIONS["type"].format(text="SecurePass!23"),
                ACTIONS["click"].format(element="submit_button"),
                ACTIONS["wait"].format(seconds=2),
                ACTIONS["verify"].format(condition="registration_complete"),
            ])
        },

        # E-commerce scenarios
        {
            "instruction": "You are a browser automation agent. Given a web task, output the sequence of actions to complete it.",
            "input": f"Task: Add product to wishlist\nCurrent page: product_page\nAvailable elements: wishlist_button, share_button, compare_button, reviews_section",
            "output": "\n".join([
                ACTIONS["scrollTo"].format(position="product_actions"),
                ACTIONS["hover"].format(element="wishlist_button"),
                ACTIONS["click"].format(element="wishlist_button"),
                ACTIONS["wait"].format(seconds=0.5),
                ACTIONS["verify"].format(condition="added_to_wishlist"),
            ])
        },

        # Navigation scenarios
        {
            "instruction": "You are a browser automation agent. Given a web task, output the sequence of actions to complete it.",
            "input": f"Task: Navigate through menu hierarchy\nCurrent page: main_menu\nAvailable elements: electronics_menu, laptops_category, gaming_laptops, filter_options",
            "output": "\n".join([
                ACTIONS["hover"].format(element="electronics_menu"),
                ACTIONS["wait"].format(seconds=0.3),
                ACTIONS["click"].format(element="laptops_category"),
                ACTIONS["wait"].format(seconds=1),
                ACTIONS["click"].format(element="gaming_laptops"),
                ACTIONS["wait"].format(seconds=2),
                ACTIONS["scrollTo"].format(position="middle"),
                ACTIONS["read"].format(element="product_list"),
            ])
        },

        # Data extraction scenarios
        {
            "instruction": "You are a browser automation agent. Given a web task, output the sequence of actions to complete it.",
            "input": f"Task: Extract pricing information\nCurrent page: comparison_site\nAvailable elements: product_table, price_column, sort_dropdown, export_button",
            "output": "\n".join([
                ACTIONS["click"].format(element="sort_dropdown"),
                ACTIONS["select"].format(value="Price: Low to High"),
                ACTIONS["wait"].format(seconds=1),
                ACTIONS["scrollTo"].format(position="top"),
                ACTIONS["read"].format(element="price_1"),
                ACTIONS["scrollTo"].format(position="middle"),
                ACTIONS["read"].format(element="price_2"),
                ACTIONS["click"].format(element="export_button"),
            ])
        },

        # Payment scenarios
        {
            "instruction": "You are a browser automation agent. Given a web task, output the sequence of actions to complete it.",
            "input": f"Task: Complete purchase with saved card\nCurrent page: checkout\nAvailable elements: saved_card_radio, cvv_field, confirm_purchase, terms_checkbox",
            "output": "\n".join([
                ACTIONS["click"].format(element="saved_card_radio"),
                ACTIONS["click"].format(element="cvv_field"),
                ACTIONS["type"].format(text="123"),
                ACTIONS["click"].format(element="terms_checkbox"),
                ACTIONS["click"].format(element="confirm_purchase"),
                ACTIONS["wait"].format(seconds=3),
                ACTIONS["verify"].format(condition="purchase_complete"),
            ])
        },

        # Social media scenarios
        {
            "instruction": "You are a browser automation agent. Given a web task, output the sequence of actions to complete it.",
            "input": f"Task: Post content with hashtags\nCurrent page: social_media_compose\nAvailable elements: post_textarea, hashtag_input, media_upload, publish_button",
            "output": "\n".join([
                ACTIONS["click"].format(element="post_textarea"),
                ACTIONS["type"].format(text="Excited about the new AI developments! "),
                ACTIONS["click"].format(element="hashtag_input"),
                ACTIONS["type"].format(text="#AI #Technology"),
                ACTIONS["click"].format(element="publish_button"),
                ACTIONS["wait"].format(seconds=1),
                ACTIONS["verify"].format(condition="post_published"),
            ])
        },

        # Settings/configuration scenarios
        {
            "instruction": "You are a browser automation agent. Given a web task, output the sequence of actions to complete it.",
            "input": f"Task: Configure notification preferences\nCurrent page: settings_notifications\nAvailable elements: email_toggle, push_toggle, frequency_dropdown, save_button",
            "output": "\n".join([
                ACTIONS["click"].format(element="email_toggle"),
                ACTIONS["click"].format(element="push_toggle"),
                ACTIONS["click"].format(element="frequency_dropdown"),
                ACTIONS["select"].format(value="Daily"),
                ACTIONS["click"].format(element="save_button"),
                ACTIONS["wait"].format(seconds=1),
                ACTIONS["verify"].format(condition="settings_saved"),
            ])
        },
    ]

    return random.choice(scenarios)


def generate_dataset(num_entries: int = 100) -> List[Dict]:
    """Generate a full dataset with specified number of entries."""
    dataset = []

    for i in range(num_entries):
        entry = generate_dataset_entry()
        dataset.append(entry)

    return dataset


def save_dataset(dataset: List[Dict], filename: str = "browser_use_dataset_expanded.json"):
    """Save dataset to JSON file."""
    with open(filename, 'w') as f:
        json.dump(dataset, f, indent=2)
    print(f"Saved {len(dataset)} entries to {filename}")


if __name__ == "__main__":
    # Generate a larger dataset
    print("Generating browser use dataset...")
    dataset = generate_dataset(50)

    # Save to file
    save_dataset(dataset, "browser_use_dataset_expanded.json")

    # Print sample
    print("\nSample entry:")
    print(json.dumps(dataset[0], indent=2))
