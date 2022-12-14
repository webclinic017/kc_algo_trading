# [Localhost API for TD Ameritrade](https://stackoverflow.com/questions/58196256/localhost-api-for-td-ameritrade)

[Ask Question](https://stackoverflow.com/questions/ask)

Asked 3 years, 2 months ago

Modified [15 days ago](https://stackoverflow.com/questions/58196256/localhost-api-for-td-ameritrade?lastactivity "2022-11-28 06:17:47Z")

Viewed 8k times

7

[](https://stackoverflow.com/posts/58196256/timeline)

I was creating an API for TD Ameritrade (my first time creating or dealing with APIs) and I needed to put in my own call back URL. I know that callback URL is where the API sends information to and i heard that I can just use my localhost API. I scoured the internet and I dont know how that would work and I was wondering if i can just use [http://localhost](http://localhost/)?

Sorry if I seem like a noob because I am

- [vb.net](https://stackoverflow.com/questions/tagged/vb.net)
- [api](https://stackoverflow.com/questions/tagged/api "show questions tagged 'api'")
- [localhost](https://stackoverflow.com/questions/tagged/localhost "show questions tagged 'localhost'")

[Share](https://stackoverflow.com/q/58196256 "Short permalink to this question")

Follow

asked Oct 2, 2019 at 6:31

[

![John Rawls's user avatar](https://lh3.googleusercontent.com/-R0GDOE7yTMc/AAAAAAAAAAI/AAAAAAAAABE/7vj3DjYYxPo/photo.jpg?sz=64)

](https://stackoverflow.com/users/8045507/john-rawls)

[John Rawls](https://stackoverflow.com/users/8045507/john-rawls)

24933 silver badges88 bronze badges

[Add a comment](https://stackoverflow.com/questions/58196256/localhost-api-for-td-ameritrade# "Use comments to ask for more information or suggest improvements. Avoid answering questions in comments.")

## 4 Answers

Sorted by:

                                              Highest score (default)                                                                   Trending (recent votes count more)                                                                   Date modified (newest first)                                                                   Date created (oldest first)                              

10

[](https://stackoverflow.com/posts/58241734/timeline)

In short, yes.

Follow the excellent directions at https://www.reddit.com/r/algotrading/comments/c81vzq/td_ameritrade_api_access_2019_guide/. (Even with them, I spent excessive time on trial and error!)

Since stackoverflow has a limit of 8 links in a response, and the localhost text string looks like a link, I’m showing it with the colon replaced by a semicolon, i.e., http;//localhost to reduce the link count. Sorry.

I used the Chrome browser after first trying Brave, which did not work for, possibly because of my option selections.

Go to https://developer.tdameritrade.com/user/me/apps

Add a new app using http;//localhost (delete existing app if there is one). Copy the resulting consumer key text string (AKA client_id or OAuth User ID).

Go to [TD Ameritrade for developer | Simple Auth for Local Apps](https://developer.tdameritrade.com/content/simple-auth-local-apps), follow instructions. Note: leading/trailing blanks were inserted by MSWord due to copy/paste of the auth code, which had to be manually deleted after wasting excessive time identifying the problem. The address string looks like:

https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=http%3A%2F%2Flocalhost&client_id=ConsumerKeyTextString%40AMER.OAUTHAP

This returns a page stating the server refused to connect, but the address bar now contains a VeryLongStringOfCharacters in the address bar: https;//localhost/?code= VeryLongStringOfCharacters

Copy the contents of the address bar, go to [https://www.urldecoder.org/](https://www.urldecoder.org/), decode the above, and extract the text after “code=”. This is your **refresh_token**

Go to: [TD Ameritrade for developer | Post Access Token](https://developer.tdameritrade.com/authentication/apis/post/token-0), fill out the fields with

```vbnet
grant_type=authorization_code
refresh_token=<<blank>>
access_type=offline
code=RefreshTokenTextString
client_id=ConsumerKeyTextString@AMER.OAUTHAP
redirect_uri=http://localhost
```

Press SEND.

If the resulting page starts with **HTTP/1.1 200 OK**, you have succeeded.

[Share](https://stackoverflow.com/a/58241734 "Short permalink to this answer")

Follow

[edited Nov 28 at 6:17](https://stackoverflow.com/posts/58241734/revisions "show all edits to this post")

[

![SaravananArumugam's user avatar](https://www.gravatar.com/avatar/5bd9ed26187f207a3dd123609d2035d6?s=64&d=identicon&r=PG)

](https://stackoverflow.com/users/402814/saravananarumugam)

[SaravananArumugam](https://stackoverflow.com/users/402814/saravananarumugam)

3,63066 gold badges3232 silver badges4545 bronze badges

answered Oct 4, 2019 at 18:45

[

![user6534901's user avatar](https://www.gravatar.com/avatar/e7e0b603e300d29e777688120e479833?s=64&d=identicon&r=PG&f=1)

](https://stackoverflow.com/users/6534901/user6534901)

[user6534901](https://stackoverflow.com/users/6534901/user6534901)

11611 silver badge33 bronze badges

- Something has changed, these instructions don't work anymore. The resulting page is a 400 error. I have doublechecked that I have followed the instructions to the letter. The code and redirect uri are correct down to the character. All I get is `{ "error": "invalid_grant" }`. I've been working on this for over a month now, just trying to authenticate successfully. I've tried every possible combination of variations, followed all instructions to the letter. I believe their API is broken. 
  
  – [John Smith](https://stackoverflow.com/users/4674841/john-smith "198 reputation")
  
   [Nov 6, 2021 at 5:41](https://stackoverflow.com/questions/58196256/localhost-api-for-td-ameritrade#comment123492241_58241734)
