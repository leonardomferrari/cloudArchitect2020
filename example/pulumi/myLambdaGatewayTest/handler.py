def handler(event, context): 
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': '"Hi from Python lambda"'
    }


const pythonLambda = new aws.lambda.Function("aws-hellolambda-python", {
    runtime: aws.lambda.Python3d6Runtime,
    code: new pulumi.asset.AssetArchive({
        ".": new pulumi.asset.FileArchive("./python"),
    }),
    timeout: 5,
    handler: "handler.handler",
    role: role.arn
});