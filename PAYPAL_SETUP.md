# PayPal Donation Setup Guide

This guide will help you set up PayPal donations for your Parent Enrichment Program website.

## Step 1: Get Your PayPal Business Account

1. Sign up for a PayPal Business account at https://www.paypal.com/business
2. Verify your account and complete the setup process
3. Note your PayPal business email address (you'll need this)

## Step 2: Set Up PayPal Donation Buttons

### Option A: Quick Donate Buttons (Preset Amounts)

1. Log into your PayPal account
2. Go to **Tools** → **All Tools** → **PayPal Buttons**
3. Click **Create a Button**
4. Select **Donate** as the button type
5. For each preset amount ($25, $50, $100, $250):
   - Set the donation amount
   - Set button name (e.g., "Parent Enrichment - $25")
   - Click **Create Button**
   - Copy the **Hosted Button ID** (looks like: `XXXXXXXXXXXXX`)
6. Replace the placeholder button IDs in `templates/donate.html`:
   - Find `YOUR_PAYPAL_BUTTON_ID_25` and replace with your $25 button ID
   - Find `YOUR_PAYPAL_BUTTON_ID_50` and replace with your $50 button ID
   - Find `YOUR_PAYPAL_BUTTON_ID_100` and replace with your $100 button ID
   - Find `YOUR_PAYPAL_BUTTON_ID_250` and replace with your $250 button ID

### Option B: Custom Amount Form

1. In `templates/donate.html`, find the line:
   ```html
   <input type="hidden" name="business" value="YOUR_PAYPAL_EMAIL@example.com" />
   ```
2. Replace `YOUR_PAYPAL_EMAIL@example.com` with your actual PayPal business email address

## Step 3: Configure Return URLs (Optional but Recommended)

The return URLs are already configured in the form to redirect back to your donate page with success/cancel messages. Make sure your Flask app URL is correct in the form.

## Step 4: Test Your Integration

1. Use PayPal's Sandbox mode to test donations without real money
2. Go to https://developer.paypal.com/
3. Create a sandbox account for testing
4. Test the donation flow end-to-end
5. Once testing is complete, switch to live mode

## Step 5: Security Considerations

- Never commit your actual PayPal email or button IDs to public repositories
- Consider using environment variables for sensitive information
- Enable PayPal IPN (Instant Payment Notification) for production to verify payments server-side

## Additional Resources

- [PayPal Button Manager](https://www.paypal.com/buttons)
- [PayPal Developer Documentation](https://developer.paypal.com/docs/)
- [PayPal Sandbox Testing](https://developer.paypal.com/docs/api-basics/sandbox/)

## Troubleshooting

- **Buttons not working**: Make sure you've replaced all placeholder values
- **Payments not going through**: Verify your PayPal account is active and verified
- **Return URL issues**: Check that your Flask app URL matches the return URL in the form



