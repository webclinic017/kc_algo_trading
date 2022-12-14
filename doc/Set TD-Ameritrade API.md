To set the API from TD-ameritrade 

- You need to apply the TD-Ameritrade Dev Accout via https://developer.tdameritrade.com/

- You need to open the My App with `redirect_uri='http://localhost'` via https://developer.tdameritrade.com/user/me/apps

- by creating the app, you will have the client-id (client key) which is important 

- <img src="file:///Users/kentchiu/Library/Application%20Support/marktext/images/2022-12-13-22-33-53-image.png" title="" alt="" width="809">





To this far, we then can generate the token and use the API. In following section, I will first share the standard process of how to generate token and then introduce the short cut of using a library. 



First, the first time the authentication process is different. By  https://developer.tdameritrade.com/content/authentication-faq

- First it will link normal TD account to app in TD-dev account

- <img src="file:///Users/kentchiu/Library/Application%20Support/marktext/images/2022-12-13-23-04-30-image.png" title="" alt="" width="385"> 

- It will provide the access-code via a URL, notice that it usually will shows error on web-page, but no worry. You just need the URL. 

- Then we are able to generate the token for our bot trading, via [TD Ameritrade for developer | Post Access Token](https://developer.tdameritrade.com/authentication/apis/post/token-0)

- There are 2 kind of token
  
  - `access token`: the token that allows you get/put data to TD API. Only live for 30 mins
  
  - `refresh token`: the token for you to get the `access token`. Live for 90 days.

- Notice that the token will be granted by URL, after you link the token to



Automate the process 

- Install the library from # https://github.com/areed1192/td-ameritrade-api

- Here I made some customiz on `from_workflow`, that it will generate `credencial.json` . (keep it in a secure place)

- Run the sample code to get the first token from library
