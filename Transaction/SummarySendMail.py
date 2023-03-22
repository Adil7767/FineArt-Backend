from django.core.mail import EmailMessage


def send_monthly_summary_report(user_email):
    # create a message object with subject and body
    subject = "Monthly Summary Report"
    body = "Please find attached your monthly summary report."
    email = EmailMessage(subject, body, 'from@example.com', [user_email])

    # attach the PDF file to the email
    with open(f'/home/shahzad/Documents/clone_Api/pdf/send_data_to_user/{user_email}_MonthlySummaryReport.pdf', 'rb') as file:
        email.attach(f'{user_email}_MonthlySummaryReport.pdf', file.read(), 'application/pdf')

    # send the email
    email.send()
    print(f"Monthly summary report sent to {user_email}")