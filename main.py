import mysql.connector
import streamlit as st
import random
from streamlit_extras.switch_page_button import switch_page
import subprocess
import manager
from st_pages import Page, show_pages, hide_pages

show_pages([
    Page("main.py", "Main"),
    Page("manager.py", "Manager"),
    Page("admin.py", "Admin")
])

hide_pages([

    'Manager',
    'Admin'
])


# Establishing a connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Rish@2812#$",
    database="mini_project"
)

mycursor = db.cursor()
print("Connection Established")

def check_admin_credentials(admin_id):
    # You should implement your logic here to check if the manager_id is valid
    # For example, you can query your database to check if the manager_id exists
    sql_check_admin = "SELECT 1 FROM admin WHERE admin_id = %s"
    mycursor.execute(sql_check_admin, (admin_id,))
    if mycursor.fetchone():
        return True  # Manager ID is valid
    else:
        return False


def check_manager_credentials(manager_id):
    # You should implement your logic here to check if the manager_id is valid
    # For example, you can query your database to check if the manager_id exists
    sql_check_manager = "SELECT 1 FROM Manager WHERE manager_id = %s"
    mycursor.execute(sql_check_manager, (manager_id,))
    if mycursor.fetchone():
        return True  # Manager ID is valid
    else:
        return False

# Create streamlit app
def main():

    if "session_srn" not in st.session_state:
        st.session_state.session_srn = None
    if "session_company_name" not in st.session_state:
        st.session_state.session_company_name = None


    st.title("Internship Portal")

    # Display options for Operations
    option = st.sidebar.selectbox("Select User Role", ("Admin", "Manager", "Student"))

    # Get query parameters to control page navigation
    params = st.experimental_get_query_params()
    current_page = params.get("page", ["student"])[0]

    # Perform selected operations
    if option == "Admin":
        st.subheader("Admin Operations")
        admin_id = st.text_input("Enter Admin ID")
        if st.button("Login"):  # Add a submit button
            # Check the manager's credentials
            if check_admin_credentials(admin_id):
               
                switch_page("Admin")

                # Navigate to the manager page after successful login
                
                 
                  # Replace "/manager.py" with the correct URL for your manager page
            else:
                st.error("Invalid Manager ID")

    elif option == "Manager":
        st.subheader("Manager Operations")
        manager_id = st.text_input("Enter Manager ID")
        if st.button("Login"):  # Add a submit button
            # Check the manager's credentials
            if check_manager_credentials(manager_id):
                switch_page("Manager")

                # Navigate to the manager page after successful login
                
                 
                  # Replace "/manager.py" with the correct URL for your manager page
            else:
                st.error("Invalid Manager ID")
        
        
        
    elif option == "Student":
        if current_page == "student":
            st.subheader("Student Operations")

            form = st.form(key="student_form")
            Name = form.text_input("Enter your Name")
            SRN = form.text_input("Enter your SRN")
            Phone_no = form.text_input("Enter your Phone Number")
            Email = form.text_input("Enter your Email Address")

            has_errors = False  # Flag to track errors
            if form.form_submit_button("Submit"):
                if not (Name and SRN and Phone_no and Email):
                    st.error("Please fill in all the compulsory fields (Name, SRN, Phone Number, Email).")
                    has_errors = True  # Set the flag to True if there are errors
                if not has_errors:  # Check if there are no errors
                    sql = "INSERT INTO Student (Name, SRN, Phone_no, Email) VALUES (%s, %s, %s, %s)"
                    values = (Name, SRN, Phone_no, Email)
                    mycursor.execute(sql, values)
                    mycursor.execute("INSERT INTO Application(SRN) VALUES(%s)",(SRN,))
                    db.commit()
                    st.experimental_set_query_params(page="application")  # Navigate to the "application" page
                    st.session_state.session_srn = SRN
                    return  # Exit the current page
        
        if current_page == "application":
            st.subheader("Student Application")
            SRN = st.session_state.session_srn
            
            form2 = st.form(key="application_form")
            
            uploaded_file = form2.file_uploader("Upload PDF Form of the Application")
            internship_title = form2.text_input("Enter your internship title")
            internship_type = form2.radio("Choose your interndship type",["On Campus Paid","On Campus Unpaid","Off Campus Paid","Off Campus Unpaid"])
            Company_name = form2.text_input("Enter Company Name (if On Campus internship, enter the college name)")
            website_link = form2.text_input("Enter the companty website link")
            start_date = form2.date_input("Enter Start Date")
            end_date = form2.date_input("Enter End Date")

            duration = (end_date - start_date).days

            function_query = f"SELECT GetTotalDurationForStudent('{SRN}')"
            mycursor.execute(function_query)
            result = mycursor.fetchone()
            print("Total Duration:", result[0])

            has_errors = False  # Flag to track errors
            if form2.form_submit_button("Submit"):
                if not (uploaded_file and internship_title and internship_type and Company_name and start_date and end_date):
                    st.error("Please fill in all the compulsory fields (File Upload, Internship Title, Internship Type, SRN).")
                    has_errors = True  # Set the flag to True if there are errors
                if not has_errors:  # Check if there are no errors
                    mycursor.execute("INSERT INTO COMPANY (company_name, website_link) values (%s, %s) ", (Company_name,website_link))
                    sql = "INSERT INTO Internship (Title, start_date, end_date, Duration, Type, company_name, SRN ) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    values = (internship_title, start_date, end_date, duration, internship_type, Company_name, SRN)
                    mycursor.execute(sql, values)
                    
                    db.commit()
                    st.session_state.session_company_name =  Company_name
                    st.success("Submitted successfully. Duration: {} days".format(duration))

            # Add a "Next" button to navigate to the "manager_info" page
            if st.button("Next"):
                st.experimental_set_query_params(page="manager_info")
            if st.button("Back"):
                st.experimental_set_query_params(page="student")
        
        if current_page == "manager_info":
            st.subheader("Manager Information")
            SRN = st.session_state.session_srn
            Company_name = st.session_state.session_company_name
            
            form3 = st.form(key="manger_form")
            Manager_Name = form3.text_input("Enter your Name")
            
            Manager_Phone_no = form3.text_input("Enter your Phone Number")
            Manager_Email = form3.text_input("Enter your Email Address")
            #Manager_id = random.randint(100000, 999999)

            has_errors = False  # Flag to track errors
            if form3.form_submit_button("Submit"):
                if not (Manager_Name and Manager_Phone_no and Manager_Email):
                    st.error("Please fill in all the compulsory fields (Name, SRN, Phone Number, Email).")
                    has_errors = True  # Set the flag to True if there are errors
                if not has_errors:  # Check if there are no errors
                    mycursor.execute("SELECT manager_id FROM Manager WHERE manager_email = %s", (Manager_Email,))
                    existing_manager_id = mycursor.fetchone()
                    if existing_manager_id:
                        Manager_id = existing_manager_id[0]
                        mycursor.execute("INSERT INTO manager_srn_map VALUES (%s,%s)",(Manager_id,SRN))
                        db.commit()
                    else:
                        Manager_id = random.randint(100000, 999999)
                        sql = "INSERT INTO Manager (manager_id,manager_phone_no, manager_name, manager_email, company_name) VALUES (%s, %s, %s, %s, %s)"
                        values = (Manager_id,Manager_Phone_no,Manager_Name,Manager_Email,Company_name)
                        mycursor.execute(sql, values)
                        mycursor.execute("INSERT INTO manager_srn_map VALUES (%s,%s)",(Manager_id,SRN))

                        db.commit()
                    st.success("Submitted successfully! Thank you for filling out for application")
            # Add a "Back" button to navigate back to the "application" page
            if st.button("Back"):
                st.experimental_set_query_params(page="application")  # Navigate back to the "application" page
    
        # Use subprocess to run manager.py
       

if __name__ == "__main__":
    main()
