# Email Compliance Fix Guide

## Current Issue
Your sender `awuleynovember@gmail.com` is using a freemail domain which violates Google, Yahoo, and Microsoft's new sender requirements.

## Required Actions

### 1. Get a Custom Domain
- Purchase a domain like `enontinoclothing.com` 
- Or use an existing domain you own
- Recommended registrars: Namecheap, GoDaddy, Google Domains

### 2. Set Up Email Authentication with Brevo

Since you're using Brevo SMTP, follow these steps:

#### A. Add Your Domain to Brevo
1. Log into your Brevo account
2. Go to **Senders, Domains & Dedicated IPs** > **Domains**
3. Click **Add a domain**
4. Enter your domain (e.g., `enontinoclothing.com`)

#### B. Configure DNS Records
Brevo will provide you with DNS records to add to your domain:

**SPF Record** (TXT record):
```
v=spf1 include:spf.brevo.com ~all
```

**DKIM Record** (TXT record):
Brevo will provide a specific DKIM key for your domain

**DMARC Record** (TXT record):
```
v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com
```

#### C. Verify Domain
- Add the DNS records to your domain
- Wait for DNS propagation (up to 48 hours)
- Verify the domain in Brevo

### 3. Create Professional Email Address
Set up email forwarding or mailbox for:
- `orders@enontinoclothing.com` (for order confirmations)
- `support@enontinoclothing.com` (for customer support)
- `noreply@enontinoclothing.com` (for automated emails)

### 4. Update Application Configuration

Update your environment variables:

```env
# Replace in .env and .env.production
DEFAULT_FROM_EMAIL=ENTstore <orders@enontinoclothing.com>
ADMIN_EMAIL=orders@enontinoclothing.com
```

### 5. Update Brevo Sender
1. In Brevo, go to **Senders**
2. Add new sender with your custom domain email
3. Verify the sender
4. Remove or disable the Gmail sender

## Quick Fix Options

### Option 1: Use Brevo's Domain (Temporary)
If you need immediate compliance, you can use Brevo's shared domain:
- Create sender like `entstore@mail.brevo.com`
- This is compliant but less professional

### Option 2: Free Custom Domain Setup
If budget is a concern:
1. Get a free domain from Freenom (.tk, .ml, .ga)
2. Use Cloudflare for free DNS management
3. Set up email forwarding through Cloudflare

## Implementation Steps

1. **Immediate**: Update sender to use Brevo domain
2. **Short-term**: Purchase custom domain and set up DNS
3. **Long-term**: Set up professional email infrastructure

## Testing
After setup, test email deliverability:
- Send test emails to Gmail, Yahoo, Outlook
- Check spam folders
- Use tools like Mail Tester to verify setup

## Benefits of Compliance
- ✅ Better email deliverability
- ✅ Professional appearance
- ✅ Compliance with major email providers
- ✅ Reduced spam filtering
- ✅ Brand trust and recognition