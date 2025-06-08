def generate_mom_html(mom_data):
    header = mom_data.get("meeting_header", {})
    participants = mom_data.get("participants", {})
    discussion_points = mom_data.get("discussion_points", {})
    additional = mom_data.get("additional", {})
    #participants = mom_data["participants"]
    #discussions = mom_data["discussion_points"]
    #additional = mom_data["additional_info"]

    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
            }}
            h1, h2 {{
                color: #2F4F4F;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }}
            th, td {{
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Minutes of Meeting</h1>
        <h2>Meeting Information</h2>
        <table>
            <tr><th>Project</th><td>{header.get('project_name', 'N/A')}</td></tr>
            <tr><th>Project</th><td>{header.get('meeting_subject', 'N/A')}</td></tr>
            <tr><th>Project</th><td>{header.get('meeting_date', 'N/A')}</td></tr>
            <tr><th>Project</th><td>{header.get('meeting_time', 'N/A')}</td></tr>
            <tr><th>Project</th><td>{header.get('venue', 'N/A')}</td></tr>
            <tr><th>Project</th><td>{header.get('mom_number', 'N/A')}</td></tr>
            <tr><th>Project</th><td>{header.get('minutes_by', 'N/A')}</td></tr>
        </table>

        <h2>Participants</h2>
        <table>
            <tr><th>Sl. No</th><th>Organization</th><th>Name</th></tr>
    """
    for p in participants:
        html += f"<tr><td>{p['sl_no']}</td><td>{p['consultant_organization']}</td><td>{p['participant_name']}</td></tr>"

    html += """
        </table>
        <h2>Discussion Points</h2>
        <table>
            <tr><th>Sl. No</th><th>Topic</th><th>Decision</th><th>Responsible</th><th>Target Date</th></tr>
    """
    for d in discussion_points:
        html += f"<tr><td>{d['sl_no']}</td><td>{d['topic_head']}</td><td>{d['discussion_decision']}</td><td>{d['responsible_team']}</td><td>{d['target_date']}</td></tr>"

    html += f"""
        </table>
        <h2>Additional Information</h2>
        <table>
            <tr><th>Project</th><td>{header.get('project_name', 'N/A')}</td></tr>
            <tr><th>Distribution List</th><td>{additional.get('distribution_list',"N/A")}</td></tr>
            <tr><th>Distribution List</th><td>{additional.get('attachments',"N/A")}</td></tr>
            #<tr><th>Distribution List</th><td>{additional.get("date", "N/A")}</td></tr>
            <tr><th>Distribution List</th><td>{additional.get('time', "N/A")}</td></tr>
            <tr><th>Response Deadline</th><td>{additional.get('response_deadline', "N/A")}</td></tr>
        </table>
    </body>
    </html>
    """
    return html
