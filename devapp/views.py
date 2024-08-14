from django.core.mail import send_mail
from django.shortcuts import render
from .forms import UploadForm
import pandas as pd

def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
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
            }
            
            # Prepare the email content
            email_subject = 'Python Assignment - Vanga Ashok'
            email_body = f"""
            Summary Report:
            
            Total Rows: {summary['total_rows']}
            Total Columns: {summary['total_columns']}
            Column Names: {', '.join(summary['column_names'])}

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
            
            return render(request, 'summary.html', {'summary': summary})
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})
