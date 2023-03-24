# cs350h

# How to run locally
1. Run 'source ~cs304flask/pub/downloads/venv/bin/activate' in command line
2. Run 'python app.py' in command line


Git checkout origin/<yourname>

## PULL
Git pull origin master

## MERGE WITH MASTER BRANCH
git checkout origin/master
git merge origin/eden -m “merge”
git push origin HEAD:master

## PUSHING CHANGES ON YOUR OWN BRANCH:
Git add -A (all changes) OR git add . (the folder you are working in)
Git commit -m “message”
Git push origin <yourname>

git merge origin/master -m “merge”