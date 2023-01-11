# NYT Leaderboard Project

## How to Debug NTY Login
Go to login page of new york times
`ctrl+shift+c` to open up dev tools in Brave
run `window.addEventListener("beforeunload", function() { debugger; }, false)` in the console
login and look at the network tab to see the requests and their responses

## Get the Cookie
![screencap of how to get the cookie](/cookie_step.png)

## How to Commit Changes
`git status` to see what has changed, and to make sure it looks right
`git diff` if you want to see the changes in files
`git add .` to stage all changes (swap the `.` to folder or file names to be more precise)
`git commit -m "{{YOUR_COMMIT_MESSAGE}}"` to commit your changes with `YOUR_COMMIT_MESSAGE` as the commit message (reminder: standard convention is to write in present tense, e.g. "Change code" vs "Changed code")
