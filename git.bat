cd ../jasima
set user=%1
set repo=%2
set token=%3
git init
git add .
git remote add origin https://github.com/%user%/%repo%.git
git commit -m "Updating repo"
git push https://%token%@github.com/%user%/%repo%.git
::pause