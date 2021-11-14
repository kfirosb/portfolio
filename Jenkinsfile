pipeline {
       environment {
            TAG="1.0"
            registry = '333923656856.dkr.ecr.eu-central-1.amazonaws.com'
            registryCredential = 'ECR'
            VER = 1.0
            AWS_DEFAULT_REGION="eu-central-1"
            OUTPUT="json"
            awsssh= "ec2-user@ec2-3-70-24-128.eu-central-1.compute.amazonaws.com"
            ec2ip = "3.70.24.128"
            PUBLICIP= ""
            IAM="333923656856"
            branch = "${BRANCH_NAME}"
    
            }
    agent any
    // options{
    //     gitLabConnection('toxiclb')
    //     timestamps()
    // }
    // triggers{
    //     gitlab(triggerOnPush: true, triggerOnMergeRequest: true, branchFilterType: 'All')
    // }
    stages {
        // stage('get_commit_msg') {
        //     steps {
        //         script {
        //             env.GIT_COMMIT_MSG = sh (script: 'git log -1 --pretty=%B ${GIT_COMMIT}', returnStdout: true).trim()
        //         }
        //     }
        // }
        stage('build') {
                    steps {
                        sh """
                        docker build -t tasksapp:"${TAG}" .
                        """
                }
            }
        stage('e2e-test') {
                when { branch 'master' }
                steps {
                    sh """
                    docker-compose up -d
                    sleep 10
                    curl http://\${ec2ip}:80
                    #docker tag tasksapp:"${TAG}" 333923656856.dkr.ecr.eu-central-1.amazonaws.com/tasksapp:\${TAG} 
                    docker-compose down
                    """
                }
            }
        // stage('push to ECR') {
        //     when {
        //         changelog '.*#test*.'
        //     }
        //     steps{
        //         echo "push to ECR stage"
        //         sh 'docker tag tedsearch:1.1-SNAPSHOT 333923656856.dkr.ecr.eu-central-1.amazonaws.com/tedsearch:1.1-SNAPSHOT'
        //         withCredentials([[
        //             $class: 'AmazonWebServicesCredentialsBinding',
        //             credentialsId: "${registryCredential}",
        //             accessKeyVariable: 'AWS_ACCESS_KEY_ID',
        //             secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        //             ]]) {
        //                 sh '''
        //                 aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin ${registry}
        //                 docker push 333923656856.dkr.ecr.eu-central-1.amazonaws.com/tedsearch:1.1-SNAPSHOT
        //                 '''
        //         }
        //     }
        // }
        // stage (' Deploy') {
        //         when {
        //             changelog '.*#test*.'
        //         }   
        //         steps {
        //         withCredentials([[
        //             $class: 'AmazonWebServicesCredentialsBinding',
        //             credentialsId: "${registryCredential}",
        //             accessKeyVariable: 'AWS_ACCESS_KEY_ID',
        //             secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        //             ]]) {
        //                 sshagent(credentials:['tedsearch']) {
        //                     sh """
        //                     cd terraform
        //                     terraform init
        //                     terraform apply --auto-approve
        //                     echo "\$(terraform output "public_ip")" > publicip.txt
        //                     """
        //                 }
        //             }
         
        //         }
        // }

        // stage('e2e-test') {
        //     when { changelog '.*#test*.' }
        //     steps {
        //         sh """
        //         publicipp=\$(cat terraform/publicip.txt)
        //         curl http://\$publicipp:80
        //         """
        //     }
        // }
            
    }      
    post {
        always {
        //     withCredentials([[
        //     $class: 'AmazonWebServicesCredentialsBinding',
        //     credentialsId: "${registryCredential}",
        //     accessKeyVariable: 'AWS_ACCESS_KEY_ID',
        //     secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
        //     ]]) {
        //         sshagent(credentials:['tedsearch']) {
        //             sh """
        //             cd terraform
        //             terraform destroy --auto-approve
        //             """
        //         }
        //     }
            sh 'docker-compose down'
            deleteDir() /* clean up our workspace */

        }
        success {
                updateGitlabCommitStatus name: 'build', state: 'success'

        }
        failure {
                updateGitlabCommitStatus name: 'build', state: 'failed'
        }
    }

}