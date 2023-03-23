from Transaction.models import Add_Transaction
from celery import shared_task
import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, legal
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from account.models import User
from Transaction.SummarySendMail import send_monthly_summary_report


@shared_task(bind=True)
def regenerate_transaction(self, data):
    transaction = Add_Transaction.objects.get(id=int(data))
    new_transaction = Add_Transaction(
        type=transaction.type,
        payment_method=transaction.payment_method,
        description=transaction.description,
        category=transaction.category,
        amount=transaction.amount,
        image=transaction.image,
        created_at=datetime.datetime.now(),
        frequency=transaction.frequency
        )
    new_transaction.save()


@shared_task(bind=True)
def monthly_summary_report(self):
    today = datetime.datetime.now()
    month = today.month
    year = today.year

    # aggregate transactions by type
    transaction_of_month = Add_Transaction.objects.filter(created_at__year=year, created_at__month=month)
    summary_data_list = [
        ['User', 'Type', 'Category', 'Payment Method', 'Updated At', 'Amount', 'Frequency', 'Description']]
    for transaction in transaction_of_month:
        summary_data_list.append([
            transaction.user,
            transaction.type,
            transaction.category,
            transaction.payment_method,
            transaction.updated_at,
            transaction.amount,
            transaction.frequency,
            transaction.description
        ])

    table_data = summary_data_list

    # create a PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(legal))

    # calculate column widths and row heights based on length of data in cells
    col_widths = [150, 80, 80, 100, 120, 80, 80, 200]
    table = Table(table_data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 7),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # add the table to the PDF document
    doc.build([table])

    # save the PDF file
    with open(f'/home/shahzad/Documents/clone_Api/pdf/monthly_all_data/{month, year}-SummaryReport.pdf', 'wb') as file:
        file.write(buffer.getvalue())
    print("PDF File is Created!")


@shared_task(bind=True)
def user_monthly_summary_report(self):
    today = datetime.datetime.now()
    month = today.month
    year = today.year

    users = User.objects.all()

    # Loop through each user
    for user in users:
        if Add_Transaction.objects.filter(user=user).exists():
            transaction_of_month = Add_Transaction.objects.filter(user=user, created_at__year=year, created_at__month=month)
            summary_data_list = [
                ['User', 'Type', 'Category', 'Payment Method', 'Updated At', 'Amount', 'Frequency', 'Description']]
            for transaction in transaction_of_month:
                summary_data_list.append([
                    transaction.user,
                    transaction.type,
                    transaction.category,
                    transaction.payment_method,
                    transaction.updated_at,
                    transaction.amount,
                    transaction.frequency,
                    transaction.description
                ])

            table_data = summary_data_list

            # create a PDF document
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=landscape(legal))

            # calculate column widths and row heights based on length of data in cells
            col_widths = [150, 80, 80, 100, 120, 80, 80, 200]
            table = Table(table_data, colWidths=col_widths)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 7),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            # add the table to the PDF document
            doc.build([table])
            with open(f'/home/shahzad/Documents/clone_Api/pdf/send_data_to_user/{user.email}_MonthlySummaryReport.pdf', 'wb') as file:
                file.write(buffer.getvalue())
            send_monthly_summary_report(user.email)
