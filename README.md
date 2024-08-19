# terraform lab

[Link](https://developer.hashicorp.com/terraform/install)

**install on MAC by binary zip file**

- wget link to download the zip package
- unzip the package to get the binary folder
- echo $PATH to check the excute path
  * /usr/local/bin
- move the folder to the Path: sudo mv terraform /usr/local/bin

**install on MAC by brew**

- `brew tap hashicorp/tap`
- `brew install hashicorp/tap/terraform`

## Provisioning AWS Infrastructure with Terraform

[Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

* write - plan - apply
* golang underthehod
* providers: clouds, k8s, and so on，三大云都是官方的provider，意味着官网HCL会维护他们，还有community和认证的provider，阿里云就是认证的provider
* 组成：由block组块组成，语言是HCL
  - block type
  - lables
  - attributes

- **初始化**work directory，下载provider组件等
  - `terraform init`
  - provider plugins存在于文件夹`.terraform`中

- **AWS access key**：可以在provider组块里设置静态的认证，也可以通过export设置在环境里
```bash
# LINUX
# Run the following commands in the Linux Terminal
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_DEFAULT_REGION="ap-northeast-1"

provider "aws" {}

# WINDOWS
# Run the following commands in the Terminal (cmd.exe or Power Shell)
$Env:AWS_ACCESS_KEY_ID=""
$Env:AWS_SECRET_ACCESS_KEY=""
$Env:AWS_DEFAULT_REGION=""
```

- `terraform plan`确认部署计划
- `terraform fmt`用于格式化tf文件，格式变得易读
- `terraform apply`部署资源
- `terraform validate`用于审查代码正确性

- **删除资源**的两种方法：
  * 一种是使用`terraform destroy`
  * 一种是从config文件中移除资源
