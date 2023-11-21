import mysql.connector
import streamlit as st
import random



# Establishing a connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rish@2812#$",
    database="mini_project"
)

mycursor = db.cursor()
print("Connection Established")

# Function to check manager credentials (you need to implement this)
def check_manager_credentials(manager_id):
    # You should implement your logic here to check if the manager_id is valid
    # For example, you can query your database to check if the manager_id exists
    sql_check_manager = "SELECT 1 FROM Manager WHERE manager_id = %s"
    mycursor.execute(sql_check_manager, (manager_id,))
    if mycursor.fetchone():
        return True  # Manager ID is valid
    else:
        return False  # Manager ID is invalid
    
# Function to switch pages
def switch_page(new_page):
    st.experimental_set_query_params(page=new_page)

def main():
    st.subheader("Manager Operations")
    
    form = st.form(key="manager_form")

    # Input for SRN by the manager
    manager_srn = form.text_input("Enter Student SRN")

    confidence_rating = form.slider("1. Confidence (1-5)", min_value=1, max_value=5)
    proactive_rating = form.slider("2. Proactive approach for Continuous improvement (1-5)", min_value=1, max_value=5)
    learning_rating = form.slider("3. Ability to learn fast (1-5)", min_value=1, max_value=5)
    skill_set_rating = form.slider("4. Skill set maturity (1-5)", min_value=1, max_value=5)
    delivery_rating = form.slider("5. Delivery of work as per commitment (1-5)", min_value=1, max_value=5)
    documentation_rating = form.slider("6. Quality of documentation (1-5)", min_value=1, max_value=5)
    communication_rating = form.slider("7. Oral and Written Communication (1-5)", min_value=1, max_value=5)
    coordination_rating = form.slider("8. Coordination with your team (1-5)", min_value=1, max_value=5)
    initiative_rating = form.slider("9. Initiative to support and build rapport (1-5)", min_value=1, max_value=5)
    overall_rating = form.slider("10. Overall Rating (1-5)", min_value=1, max_value=5)

    feedback = form.text_area("Feedback")
    
    if form.form_submit_button("Submit"):
        if not (manager_srn and confidence_rating and feedback):
            st.error("Please provide SRN, rating, and feedback.")
        else:
            mycursor.execute("SELECT manager_id from manager_srn_map where SRN = %s",(manager_srn,))
            existing_mgr = mycursor.fetchone()

            if existing_mgr is not None: 
                manager_id = existing_mgr[0]
                # Check if the SRN exists in the database before submitting the review
                sql_check_srn = "SELECT 1 FROM Student WHERE SRN = %s"
                mycursor.execute(sql_check_srn, (manager_srn,))
            
                if mycursor.fetchone():
                    # Insert the review into the database with manager_id
                    rating = (confidence_rating + proactive_rating + learning_rating + skill_set_rating +
                            delivery_rating + documentation_rating + communication_rating + coordination_rating +
                            initiative_rating + overall_rating) / 10
                    sql = "INSERT INTO manager_review (manager_id, SRN, rating, feedback) VALUES (%s, %s, %s, %s)"
                    values = (manager_id, manager_srn, rating, feedback)
                    mycursor.execute(sql, values)
                    db.commit()
                    st.success("Review submitted successfully!")
                    st.write("")
                    if st.button("New Review"):
                        switch_page("manager_form")
                else:
                    st.error(f"Student with SRN {manager_srn} does not exist.")
            else:
                st.error(f"Manager with SRN {manager_srn} does not exist.")

if __name__=="__main__":
    main()
