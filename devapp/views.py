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
            
            # Select the necessary columns
            df.columns = df.columns.str.replace(' ', '_')
            selected_columns = df[['Cust_State', 'Cust_Pin', 'DPD']].dropna()

            # Generate the table content
            table_content = "\n".join(
                f"<tr><td style='border:1px solid black; border-collapse:collapse'>{row['Cust_State']}</td><td style='border:1px solid black; border-collapse:collapse'>{row['Cust_Pin']}<td style='border:1px solid black;border-collapse:collapse'>{row['DPD']} </td></tr>"
                
                
            
            for _, row in selected_columns.iterrows())
            data = [row for _, row in selected_columns.iterrows()]
            
            # Prepare the email content
            email_subject = 'Python Assignment - Vanga Ashok'
            email_body = f"""
            Summary Report:
            
            Total Rows: {summary['total_rows']}
            Total Columns: {summary['total_columns']}
            Column Names: {', '.join(summary['column_names'])}

            Detailed Table:

            State\tCust Pin\tDPD
            <table  style="border:1px solid black;border-collapse:collapse">
            <tr>
            <th style="border:1px solid black;border-collapse:collapse">State</th>
            <th style="border:1px solid black;border-collapse:collapse">Cust Pin</th>
            <th style="border:1px solid black;border-collapse:collapse">DPD</th>
            </tr>
            {table_content}
            </table>
            """
            
            # List of recipients
            recipient_list = ['ashokasmart01@gmail.com'] #, 'recipient2@example.com']
            
            # Send the email
            send_mail(
                email_subject,
                '',
                'ashokavanga@gmail.com',  # Sender's email
                recipient_list,
                fail_silently=False,
                html_message=email_body
            )
            print(type(selected_columns.iterrows()))
            return render(request, 'summary.html', {'summary': summary, 'data': data})
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})