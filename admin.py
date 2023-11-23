import mysql.connector
import streamlit as st
import pandas as pd
import smtplib
import ssl
from email.message import EmailMessage

# Establishing a connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysqlpswrd4321",
    database="mini_project"
)

def send_manager_email(manager_email, manager_id, student_srn):
    email_sender = 'trialdemo113445@gmail.com'
    email_password = 'ipnm rtch eqkc zzgg'

    subject = 'Manager Login Information for Internship'
    body = f"""
    Good Morning!
    Greetings from PES University!
    This email contains login information for the student internship for your intern at PES University
    Please refer to the following for login and provide your evaluation for the different fields provided:
    Manager ID: {manager_id}
    Student SRN: {student_srn}
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = manager_email
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, manager_email, em.as_string())
mycursor = db.cursor()
print("Connection Established")

def admin_page():
    st.title("Admin Page")

    st.write("Confirmed Applications: ")

    # Fetch submitted application details
    query_admin_page = """
        SELECT 
            A.Application_ID,
            S.SRN AS Student_SRN,
            S.Name AS Student_Name
        FROM 
            Application A
        JOIN
            Student S ON A.SRN = S.SRN
        WHERE
            A.application_status != 'pending'
    """
    mycursor.execute(query_admin_page)
    admin_results = mycursor.fetchall()

    # Convert results to DataFrame
    admin_df = pd.DataFrame(admin_results, columns=["Application_ID", "Student_SRN", "Student_Name"])

    # Display the DataFrame in Streamlit
    if not admin_df.empty:
        st.dataframe(admin_df)

    else:
        st.info("No submitted applications.")

    # Add a button to go back to the search_by_srn page
    st.button("Go Back to Search by SRN", on_click=lambda: st.experimental_set_query_params(page="search_by_srn"))

def main():

    # Get the current page from the query parameters
    params = st.experimental_get_query_params()
    current_page = params.get("page", ["search_by_srn"])[0]

    # Search by SRN
    if current_page == "search_by_srn":
        search_srn = st.text_input("Search by SRN:")
        if search_srn:
            # Query to get details based on SRN
            query_details = f"""
                SELECT
                    S.SRN AS Student_SRN,
                    S.Name AS Student_Name,
                    S.Email AS Student_Email,
                    M.manager_ID,
                    M.manager_name,
                    M.manager_email,
                    MR.Rating AS Manager_Rating,
                    MR.Feedback AS Manager_Feedback,
                    I.start_date AS Internship_Start_Date,
                    I.end_date AS Internship_End_Date,
                    I.Title AS Internship_Title,
                    I.Type AS Internship_Type,
                    C.company_name,
                    C.website_link
                FROM
                    Student S
                JOIN
                    manager_srn_map MMap ON S.SRN = MMap.SRN
                JOIN
                    Manager M ON MMap.manager_ID = M.manager_ID
                JOIN
                    Internship I ON S.SRN = I.SRN
                JOIN
                    Company C ON I.company_name = C.company_name
                LEFT JOIN
                    Manager_Review MR ON M.manager_ID = MR.manager_ID
                WHERE
                    S.SRN = '{search_srn}'; 
                """

            # Execute the query
            mycursor.execute(query_details)
            result = mycursor.fetchall()

            if result:
                st.markdown("""<style>div.Widget.row-widget.stRadio > div{flex-direction: column; border: 2px solid #ddd; border-radius: 8px; padding: 10px;}</style>""", unsafe_allow_html=True)
                st.title("Student and Manager Information:")
                st.subheader("Student Details:")
                st.write(f"- SRN: {result[0][0]}")
                st.write(f"- Name: {result[0][1]}")
                st.write(f"- Email: {result[0][2]}")

                st.subheader("Manager Details:")
                st.write(f"- Manager ID: {result[0][3]}")
                st.write(f"- Manager Name: {result[0][4]}")
                st.write(f"- Manager Email: {result[0][5]}")
                st.write(f"- Manager Rating: {result[0][6]}")
                st.write(f"- Manager Feedback: {result[0][7]}")

                st.subheader("Internship Details:")
                st.write(f"- Start Date: {result[0][8]}")
                st.write(f"- End Date: {result[0][9]}")
                st.write(f"- Title: {result[0][10]}")
                st.write(f"- Type: {result[0][11]}")

                st.subheader("Company Details:")
                st.write(f"- Company Name: {result[0][12]}")
                st.write(f"- Company Website: {result[0][13]}")
                st.markdown("""<style>div.Widget.row-widget.stButton > div{border: 2px solid #ddd; border-radius: 8px; padding: 10px;}</style>""", unsafe_allow_html=True)

                if st.button("Send Manager Email"):
                    email = result[0][5]
                    managerid = result[0][3]
                    srn = result[0][0]
                    send_manager_email(email,managerid,srn)
                # Approval/Disapproval functionality
                action = st.radio("Action", ["Approve", "Disapprove"])

                if st.button("Submit"):
                    SRN = str(result[0][0])  # Convert to standard Python integer
                    if action == "Approve":
                        # Update application status to 'completed'
                        mycursor.execute("UPDATE Application SET application_status = 'completed' WHERE SRN = %s", (SRN,))
                        db.commit()
                        st.success(f"Application for SRN {SRN} Approved!")

                    elif action == "Disapprove":
                        # Update application status to 'not completed'
                        mycursor.execute("UPDATE Application SET application_status = 'not completed' WHERE SRN = %s", (SRN,))
                        db.commit()
                        st.warning(f"Application for SRN {SRN} Disapproved!")

                    # Add a button to go to the admin page
                    st.button("Go to Admin Page", on_click=lambda: st.experimental_set_query_params(page="admin"))

            else:
                st.warning("No data available for the provided SRN.")
        else:
            # Radio buttons to switch between views
            view_option = st.radio("Select View Option", ["All Entries", "Pending Manager Review Status", "Pending Application Status"])

            # View for all entries with pending manager review status
            query_pending_manager_review = """
            SELECT 
                Application_ID,
                SRN AS Student_SRN
            FROM 
                Application
            WHERE
             manager_review_status = 'pending'
            """

            # View for all entries with pending application status
            query_pending_application = """
            SELECT 
                Application_ID,
                SRN AS Student_SRN
            FROM 
                Application
            WHERE
                application_status = 'pending'
            """

            # Default view (no radio button selected)
            query_default = """
            SELECT 
                Application_ID,
                SRN AS Student_SRN
            FROM 
                Application    
            """

            # Execute the query based on radio button selection
            if view_option == "Pending Manager Review Status":
                mycursor.execute(query_pending_manager_review)
                results = mycursor.fetchall()
                if not results:
                    st.warning("No data available for pending manager review status.")
                else:
                    st.title("Pending Manager Review Status:")
            elif view_option == "Pending Application Status":
                mycursor.execute(query_pending_application)
                results = mycursor.fetchall()
                if not results:
                    st.warning("No data available for pending application status.")
                else:
                    st.title("Pending Application Status:")
            else:
                # Default view (All Entries)
                st.title("Student Records")
                mycursor.execute(query_default)
                results = mycursor.fetchall()

            # Convert results to DataFrame
            df = pd.DataFrame(results, columns=["Application_ID", "Student_SRN"])

            # Display the DataFrame in Streamlit
            if not df.empty:
                st.dataframe(df)

    elif current_page == "admin":
        admin_page()

if __name__ == "__main__":
    main()
