import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope: allows read and write access
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    """Authenticate the user and return Gmail API credentials."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def clean_promotions(service):
    """Delete emails labeled as 'Promotions' (CATEGORY_PROMOTIONS)."""
    results = service.users().messages().list(userId='me', labelIds=['CATEGORY_PROMOTIONS'], maxResults=100).execute()
    messages = results.get('messages', [])

    print(f"Found {len(messages)} promotional emails.")
    for msg in messages:
        service.users().messages().delete(userId='me', id=msg['id']).execute()
    print("Promotional emails deleted.")

def clean_unread_older_than_30_days(service):
    """Delete unread emails older than 30 days."""
    results = service.users().messages().list(userId='me', q='is:unread older_than:30d', maxResults=100).execute()
    messages = results.get('messages', [])

    print(f"Found {len(messages)} unread emails older than 30 days.")
    for msg in messages:
        service.users().messages().delete(userId='me', id=msg['id']).execute()
    print("Old unread emails deleted.")

def clean_from_specific_sender(service, sender_email):
    """Delete emails from a specific sender."""
    query = f"from:{sender_email}"
    results = service.users().messages().list(userId='me', q=query, maxResults=100).execute()
    messages = results.get('messages', [])

    print(f"Found {len(messages)} emails from {sender_email}.")
    for msg in messages:
        service.users().messages().delete(userId='me', id=msg['id']).execute()
    print(f"Emails from {sender_email} deleted.")


def trash_by_label(service, label_name):
    """
    Move to trash all emails that have a specific label (including sublabels).
    Example label_name: 'society-academia' (represents society/academia)
    """
    # Step 1: Get all labels
    labels = list_all_labels(service)

    # Step 2: Match the label ID
    label_id = None
    for label in labels:
        if label['name'].lower() == label_name.lower():
            label_id = label['id']
            break

    if not label_id:
        print(f"Label '{label_name}' not found.")
        return

    # Step 3: Get messages with that label
    results = service.users().messages().list(userId='me', labelIds=[label_id], maxResults=500).execute()
    messages = results.get('messages', [])

    print(f"Found {len(messages)} emails with label '{label_name}'.")

    # Step 4: Move each to trash
    for msg in messages:
        try:
            service.users().messages().trash(userId='me', id=msg['id']).execute()
        except Exception as e:
            print(f"Failed to trash message {msg['id']}: {e}")

    print(f"Emails with label '{label_name}' moved to trash.")

def list_all_labels(service):
    labels_response = service.users().labels().list(userId='me').execute()
    labels = labels_response.get('labels', [])
    for label in labels:
        print(f"{label['name']} → {label['id']}")
    return labels

def archive_emails(service, query):
    """Archive emails (remove them from the inbox) instead of deleting."""
    results = service.users().messages().list(userId='me', q=query, maxResults=100).execute()
    messages = results.get('messages', [])

    print(f"Found {len(messages)} emails to archive (query: {query}).")
    for msg in messages:
        service.users().messages().modify(
            userId='me',
            id=msg['id'],
            body={'removeLabelIds': ['INBOX']}
        ).execute()
    print("Emails archived.")

def main():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    # === Choose which actions to perform ===
    
    # clean_promotions(service)
    # clean_unread_older_than_30_days(service)
    # clean_from_specific_sender(service, 'noreply@example.com')
    # archive_emails(service, 'label:ads')  # you can change the query as needed
    # trash_by_label(service, 'society/Facebook')  # <- this one is enabled
    list_all_labels(service)

if __name__ == '__main__':
    main()
