# SudokuServerless
A serverless website with a sudoku theme, based on [Build a Serverless Web App...](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/).


### Quick start
Create the website:
```
hugo new site sudoku-serverless-hugo
git init
```

Add a theme:
```
git submodule add git@github.com:Alex-Burgess/kube.git sudoku-serverless-hugo/themes/kube
```

Copy and Update the config:
```
cp themes/kube/exampleSite/config.toml .
```

Create main stack:
```
aws cloudformation create-stack --stack-name Sudoku-Serverless-Main --template-body file://main.yaml
```

Build and Copy website content:
```
hugo
aws s3 sync public/ s3://sudoku-serverless --delete
```

Update stack:
```
aws cloudformation update-stack --stack-name Sudoku-Serverless-Main --template-body file://main.yaml
```

Add data to sudoku unsolved puzzles bucket:
```
aws s3 cp data/example_puzzles/ s3://sudoku-unsolved-puzzles --recursive
```

# Reference
To do.
