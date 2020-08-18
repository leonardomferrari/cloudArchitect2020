
module "ecs-cluster" {
  source = "./modules/ecs-cluster"
}

module "lambda" {
  source = "./modules/lambda"
}

module "glue-crawlers" {
  source = "./modules/glue-crawlers"
}

module "glue-jobs" {
  source = "./modules/glue-jobs"
}

module "measurements-crawler" {
  source = "./modules/measurements-crawler"
}
