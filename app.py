from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Load environment variables
load_dotenv()  

# Set page configuration
st.set_page_config(page_title="I can Retrieve Any SQL query")

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Promotion questions and answers
promotions_questions = [
    "Are there any discounts on Gir Cow Ghee?",
    "Do you have any special offers today?",
    "Today's offer?",
    "Is there a sale on any products?",
    "What are the current promotions?",
    "Do you have any seasonal discounts?",
    "Are there any bulk purchase discounts?",
    "Can I get a discount if I subscribe to your newsletter?",
    "Is there a student discount available?",
    "Do you offer first-time customer discounts?",
    "Are there any loyalty rewards or points?"
]

promotions_answers = {
    "Are there any discounts on Gir Cow Ghee?": "Yes, we currently have a 10% discount on Gir Cow Ghee.",
    "Do you have any special offers today?": "Today, we have a buy one get one free offer on select products.",
    "Today's offer?": "Today, we have a buy one get one free offer on select products.",
    "Is there a sale on any products?": "Yes, we have a sale on various products, including a 10% discount on Gir Cow Ghee.",
    "What are the current promotions?": "We currently offer a 10% discount on Gir Cow Ghee and a buy one get one free offer on select products.",
    "Do you have any seasonal discounts?": "Yes, we offer seasonal discounts. Please check our website or contact support for the latest offers.",
    "Are there any bulk purchase discounts?": "Yes, we offer discounts on bulk purchases. Please contact our sales team for more details.",
    "Can I get a discount if I subscribe to your newsletter?": "Yes, subscribers to our newsletter receive exclusive discounts and offers.",
    "Is there a student discount available?": "Yes, we offer a student discount. Please provide a valid student ID to avail of this offer.",
    "Do you offer first-time customer discounts?": "Yes, first-time customers can enjoy a 5% discount on their first purchase.",
    "Are there any loyalty rewards or points?": "Yes, we have a loyalty rewards program. Earn points with every purchase and redeem them for discounts."
}

# Support questions and answers
support_questions = [
    "How do I return a product?",
    "What is your shipping policy?",
    "What payment methods do you accept?",
    "How can I track my order?",
    "Do you ship internationally?",
    "How do I cancel my order?",
    "What should I do if I receive a damaged product?",
    "How long does it take to process a refund?",
    "Can I change my shipping address after placing an order?",
    "Do you offer gift wrapping services?",
    "How do I contact customer support?"
]

support_answers = {
    "How do I return a product?": "You can return a product by contacting our support team within 30 days of purchase.",
    "What is your shipping policy?": "We offer free shipping on orders over $50. Orders are typically processed within 2-3 business days.",
    "What payment methods do you accept?": "We accept all major credit cards, PayPal, and Apple Pay.",
    "How can I track my order?": "You can track your order using the tracking number provided in your shipment confirmation email.",
    "Do you ship internationally?": "Yes, we ship internationally. Shipping costs and delivery times may vary based on location.",
    "How do I cancel my order?": "To cancel your order, please contact our customer support team as soon as possible. Orders that have already been shipped cannot be cancelled.",
    "What should I do if I receive a damaged product?": "If you receive a damaged product, please contact our support team immediately with photos of the damage.",
    "How long does it take to process a refund?": "Refunds are typically processed within 5-7 business days after we receive the returned product.",
    "Can I change my shipping address after placing an order?": "If your order has not yet been shipped, you can update your shipping address by contacting our support team.",
    "Do you offer gift wrapping services?": "Yes, we offer gift wrapping services for an additional fee. Please select the option at checkout.",
    "How do I contact customer support?": "You can contact our customer support team via email at support@gheestore.com or by calling 1-800-123-4567."
}

def get_gemini_response(question, prompt):
    # Check if the question is a promotion or support question
    if question in promotions_questions:
        return promotions_answers[question]
    elif question in support_questions:
        return support_answers[question]
    
    # Otherwise, generate SQL query
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

prompt = [
    """
    You are an expert in converting English questions to SQL query!
    The SQL database contains a table named GHEE_PRODUCTS with the following columns - PRODUCT_NAME, SALES_COUNT, PRICE, and CATEGORY.

    For example,
    Example 1 - Which ghee product is selling the most?, 
    the SQL command will be something like this SELECT PRODUCT_NAME FROM GHEE_PRODUCTS ORDER BY SALES_COUNT DESC LIMIT 1;

    Example 2 - Show me all ghee products that are under $50,
    the SQL command will be something like this SELECT * FROM GHEE_PRODUCTS WHERE PRICE < 50;

    Also, the SQL code should not have 
    in the beginning or end and the SQL word in the output.
    """
]

# Streamlit App
st.header("Gemini App To Retrieve SQL Data")

question = st.text_input("Input: ", key="input")

submit = st.button("Ask the question")
if submit:
    response = get_gemini_response(question, prompt)
    
    # Check if the response is a promotion/support answer or SQL query
    if response in promotions_answers.values() or response in support_answers.values():
        st.subheader("Answer:")
        st.write(response)
    else:
        rows = read_sql_query(response, "student.db")
        st.subheader("The Response is:")
        for row in rows:
            st.write(row)
