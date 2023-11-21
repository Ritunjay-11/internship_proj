import mysql.connector
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from st_pages import Page, show_pages, hide_pages



show_pages([
    Page("home.py", "Home"),
    Page("application_form.py", "Application")
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

# Create streamlit app
hide_pages(['Application'])


def main():
    st.title("Internship Portal")

    css_bg_color = """
        <style>
            .streamlit-container {
                background-color: #f0f0f0;  /* Replace with your desired color code */
            }
        </style>
    """
    st.markdown(css_bg_color, unsafe_allow_html=True)
    # Display options for Operations
    option = st.sidebar.selectbox("Select User Role", ("Admin", "Manager", "Student"))

    # Perform selected operations
    if option == "Admin":
        st.subheader("Admin Operations")

    elif option == "Manager":
        st.subheader("Manager Operations")

    elif option == "Student":
        st.subheader("Student Operations")

        if "submitted" not in st.session_state:
            with st.form("student_info_form"):
                st.write("Please enter your information:")
                Name = st.text_input("Name")
                SRN = st.text_input("SRN")
                Phone_no = st.text_input("Phone Number")
                Email = st.text_input("Email")

                if st.form_submit_button("Submit"):
                    if not (Name and SRN and Phone_no and Email):
                        st.error("Please fill in all the compulsory fields (Name, SRN, Phone Number, Email).")
                    else:
                        sql = "INSERT INTO Student (Name, SRN, Phone_no, Email) VALUES (%s, %s, %s, %s)"
                        values = (Name, SRN, Phone_no, Email)
                        mycursor.execute(sql, values)
                        db.commit()
                        st.session_state.submitted = True
                        st.success("Submitted successfully")
                        switch_page('Application')


if __name__ == "__main__":
    main()
