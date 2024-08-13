from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ExcelUploadForm
import pandas as pd

def upload_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded file
            excel_file = request.FILES['file']
            
            # Read the file using pandas
            df = pd.read_excel(excel_file, engine='openpyxl')
            
            # Generate summary
            summary = {
                'total_rows': df.shape[0],
                'total_columns': df.shape[1],
                'column_names': df.columns.tolist(),
                'summary_stats': df.describe().to_string(),
            }
            
            # Prepare the email content
            email_subject = 'Python Assignment - Vanga Ashok'
            email_body = f"""
            Summary Report:
            
            Total Rows: {summary['total_rows']}
            Total Columns: {summary['total_columns']}
            Column Names: {', '.join(summary['column_names'])}

            Summary Statistics:
            {summary['summary_stats']}
            """
            
            # List of recipients
            recipient_list = ['ashokasmart01@gmail.com'] #, 'recipient2@example.com']
            
            # Send the email
            send_mail(
                email_subject,
                email_body,
                'ashokavanga@gmail.com',  # Sender's email
                recipient_list,
                fail_silently=False,
            )
            
            return render(request, 'excel_summary.html', {'summary': summary})
    else:
        form = ExcelUploadForm()

    return render(request, 'upload_excel.html', {'form': form})
