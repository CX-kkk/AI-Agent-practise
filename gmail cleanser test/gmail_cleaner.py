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

def clean_from_specific_sender(service, sender_email, max_results=500):
    """Move emails from a specific sender to Trash (instead of deleting)."""
    query = f"from:{sender_email}"
    messages = []
    page_token = None
    fetched = 0

    # Fetch messages with pagination if needed
    while True:
        list_kwargs = {
            "userId": 'me',
            "q": query,
            "maxResults": min(500, max_results - fetched) if max_results else 500
        }
        if page_token:
            list_kwargs["pageToken"] = page_token

        results = service.users().messages().list(**list_kwargs).execute()
        batch = results.get('messages', [])
        messages.extend(batch)
        fetched += len(batch)
        page_token = results.get('nextPageToken')
        if not page_token or (max_results and fetched >= max_results):
            break

    if max_results:
        messages = messages[:max_results]

    total = len(messages)
    print(f"Found {total} emails from {sender_email}.")
    if total == 0:
        print("No emails to move to Trash.")
        return

    # Progress update every 20%
    progress_marks = {int(total * p / 100) for p in range(20, 101, 20)}
    if total in progress_marks:
        progress_marks.remove(total)

    for idx, msg in enumerate(messages, 1):
        service.users().messages().trash(userId='me', id=msg['id']).execute()
        if idx in progress_marks:
            percent = int(idx / total * 100)
            print(f"{percent}% done...")
    print(f"Emails from {sender_email} moved to Trash.")

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

def list_all_labels(service, if_print: bool = False):
    labels_response = service.users().labels().list(userId='me').execute()
    labels = labels_response.get('labels', [])
    if if_print:
        for label in labels:
            print(f"{label['name']} → {label['id']}")
    return labels

def trash_by_label(service, label_name, max_results=1000):
    """
    Move to trash all emails that have a specific label (including sublabels).
    Example label_name: 'society-academia' (represents society/academia)
    If max_results is given, only process up to max_results emails.
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

    # Step 3: Get messages with that label (handle pagination if needed)
    messages = []
    page_token = None
    fetched = 0
    while True:
        list_kwargs = {
            "userId": 'me',
            "labelIds": [label_id]
        }
        if max_results is not None:
            # Only fetch up to maxResults in total
            remaining = max_results - fetched
            list_kwargs["maxResults"] = min(500, remaining)
        else:
            list_kwargs["maxResults"] = 500

        if page_token:
            list_kwargs["pageToken"] = page_token

        results = service.users().messages().list(**list_kwargs).execute()
        batch = results.get('messages', [])
        messages.extend(batch)
        fetched += len(batch)
        page_token = results.get('nextPageToken')
        if not page_token or (max_results is not None and fetched >= max_results):
            break

    if max_results is not None:
        messages = messages[:max_results]

    total = len(messages)
    print(f"Found {total} emails with label '{label_name}'.")

    if total == 0:
        print(f"No emails to trash for label '{label_name}'.")
        return

    # Step 4: Move each to trash, show progress
    if total > 500:
        progress_marks = {int(total * p / 100) for p in range(1, 101)}
        if total in progress_marks:
            progress_marks.remove(total)
    else:
        progress_marks = {int(total * p / 100) for p in range(20, 101, 20)}
        if total in progress_marks:
            progress_marks.remove(total)

    for idx, msg in enumerate(messages, 1):
        try:
            service.users().messages().trash(userId='me', id=msg['id']).execute()
        except Exception as e:
            print(f"Failed to trash message {msg['id']}: {e}")
        if idx in progress_marks:
            percent = int(idx / total * 100)
            print(f"{percent}% done...")
    print(f"Emails with label '{label_name}' moved to trash.")

def main():
    creds = authenticate()
    service = build('gmail', 'v1', credentials=creds)

    # === Choose which actions to perform ===
    
    # clean_promotions(service)
    # clean_unread_older_than_30_days(service)
    clean_from_specific_sender(service, 'sandor@condos.ca')
    # archive_emails(service, 'label:ads')  # you can change the query as needed
    # trash_by_label(service, 'society/Twitter')  # <- this one is enabled
    # list_all_labels(service, if_print=True)  # List all labels

if __name__ == '__main__':
    main()
