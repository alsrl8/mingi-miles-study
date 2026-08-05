---
id: topic-mail-server-fundamentals-001
created: 2026-08-05
status: active
tags: [networking, email, smtp, imap, pop3, protocols]
source: public-ietf-rfcs
visibility: public
---

# What a mail server is, and why Gmail is not one

## Why Gmail looks like it answers the question but doesn't

Opening Gmail in a browser is opening a web application: HTML, JavaScript,
HTTPS, a REST-ish backend. That is real, but it is only the front door. Gmail
the product is a webmail client bolted onto a mail server Google also
operates. The part that makes something a "mail server" is not the compose
box; it is what happens after Miles clicks Send, when the message has to
leave Google's infrastructure and land in a mailbox Google does not control.

## The two jobs a mail system does, and why they're different protocols

Email splits into two jobs that HTTP does not need to distinguish:

1. **Getting a message from sender to the recipient's server.** This is
   store-and-forward: a message can hop through more than one server before
   it reaches its destination, and the sending server does not wait for the
   human to read it. The protocol for this is **SMTP** (Simple Mail Transfer
   Protocol), specified in **RFC 5321**. The message content itself, headers
   included, follows a separate spec: the **Internet Message Format**,
   **RFC 5322**.
2. **Getting a message out of a mailbox and onto a device a human reads.**
   This is retrieval, and it happens after storage, on demand. Two competing
   specs exist:
   - **POP3** (Post Office Protocol v3), **RFC 1939**: download-and-usually-
     delete. No concept of folders or synchronized read state across
     devices.
   - **IMAP** (Internet Message Access Protocol): the mailbox stays on the
     server, folders and read/unread flags are visible to every client that
     connects. Current version **IMAP4rev2** is **RFC 9051**, which obsoletes
     the long-lived **IMAP4rev1**, **RFC 3501**.

HTTP has no equivalent split because a web page is not relayed between
organizations and does not need a second protocol for "check if there's
anything new." A browser just re-requests the page.

## Worked example: one email, two different protocols, same message

Miles composes a message in the Gmail web app addressed to a friend on
`daum.net`.

1. Browser to Gmail: plain HTTPS. This leg is indistinguishable from using
   any other web app. No SMTP, no IMAP here.
2. Miles clicks Send. Gmail's backend now acts as a **Mail Transfer Agent**
   (MTA). It does not know which physical server handles `daum.net` mail, so
   it asks DNS for that domain's **MX record** — a record whose entire
   purpose is "which host accepts mail for this domain," separate from
   whatever host serves `www.daum.net`. That is why a company's website and
   its mail can live on completely different infrastructure with the same
   domain name.
3. Gmail's MTA opens a TCP connection to Daum's mail exchanger and speaks
   SMTP: a short line-based command exchange (`EHLO`, `MAIL FROM:`,
   `RCPT TO:`, `DATA`, then the RFC 5322 message, then `.` to end it). Daum's
   server accepts the bytes and writes them into the friend's mailbox
   storage. SMTP's job ends there — it moved the message, nothing more.
4. Later, the friend opens their mail app. The app connects to Daum's server
   over IMAP (or POP3, if it's an older or simpler client) to ask "what's in
   my mailbox" and pull the message down. This is a completely separate
   protocol session from step 3, often to a different port, sometimes to a
   different physical server.

Four different transport moments, two different jobs, and the person only
sees "I sent an email and they got it."

## Common misconception

"Email protocols are basically a web API, just for mail." Two concrete
reasons this is wrong:

- **Relay, not single-hop request/response.** An HTTP request goes to one
  server and gets one response. SMTP delivery can and does traverse more
  than one MTA hop (sender's outbound server, possibly a relay, then the
  recipient's inbound server), and each hop can independently accept,
  queue, retry, or bounce the message. There is no single server Miles's
  browser ever talks to end-to-end.
- **Envelope and header are not the same thing, and this is the point where
  spoofing lives.** SMTP's `MAIL FROM` / `RCPT TO` (the envelope) is what
  actually routes and bounces the message. The `From:` / `To:` lines inside
  the RFC 5322 content (the header) are just text in the message body, shown
  to the human reader. A server can accept a message whose envelope sender
  and header `From:` disagree entirely — HTTP has no analogous split between
  "what routed this" and "what the payload claims."

## Recall check

Miles's friend complains: "I read an email on my phone, marked it read, then
opened my laptop and it still showed as unread." Which of the two retrieval
protocols above is almost certainly configured on the laptop, and which
single property of that protocol explains the symptom? Answer before reading
further — this topic file has no hidden answer block; state your answer back
in the conversation.

## Sources

- https://datatracker.ietf.org/doc/html/rfc5321
- https://datatracker.ietf.org/doc/html/rfc5322
- https://datatracker.ietf.org/doc/html/rfc1939
- https://datatracker.ietf.org/doc/html/rfc9051
- https://datatracker.ietf.org/doc/html/rfc3501
