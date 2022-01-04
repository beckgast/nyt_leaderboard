# NYT Leaderboard Project

## How to Debug NTY Login
go to login page of new york times
`ctrl+shift+c` to open up dev tools in Brave
run `window.addEventListener("beforeunload", function() { debugger; }, false)` in the console
login and look at the network tab to see the requests and their responses

## Get the Cookie
![screencap of how to get the cookie](/cookie_step.png)