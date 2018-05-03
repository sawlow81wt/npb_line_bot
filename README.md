# npb_line_bot


NPB Latest news that prevent spoilers.

## requirement
+ Docker version 18.03.1-ce

### Certification
You need to put the certificate files fullchain.pem and key.pem in the /certs/flask/.

### enviroment variable
You need to set some environment variables. Please obtain access token and channel secret key from [LINE DEVELOPERS](https://developers.line.me).

> LINE_ACCESSS_TOKEN="YOUR_ACCESEE_TOKEN"  
> LINE_CHANNEL_SECRET="YOUR_CHANNEL_SECRET"

## usage

+ clone it.　　
> ./build

callback url is 
> https://your.server.name:5000/callback

## QR code

![](https://github.com/sawlow81wt/npb_line_bot/blob/master/img/nlp_news.png)
