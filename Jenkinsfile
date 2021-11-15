pipeline {
       environment {
            TAG="1.0.5"
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
    stages {
        stage('build') {
                    steps {
                        sh """
                        docker build -t tasksapp:"${BUILD_NUMBER}" .
                        """
                }
            }
        stage('e2e-test') {
                steps {
                    sh """
                    docker-compose up -d
                    sleep 10
                    curl http://\${ec2ip}:80
                    docker-compose down
                    """
                }
            }
        stage('tag') {
                when { anyOf { branch 'release/*'; branch 'master' } }
                steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${registryCredential}",
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                    ]]) {
                        sh """
                        aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin \${registry}
                        aws ecr list-images --repository-name tasksapp
                        if [[ \$BRANCH_NAME==master ]];
                        then
                            echo "latest" > tag.txt
                        else
                            chmod 777 pushfile.sh
                            ./pushfile.sh $BRANCH_NAME    
                        fi
                        TAG=\$(cat tag.txt)
                        docker tag tasksapp:"${BUILD_NUMBER}" 333923656856.dkr.ecr.eu-central-1.amazonaws.com/tasksapp:\$TAG
                        """
                }
            }
        }
        stage('publis') {
            when { anyOf { branch 'release/*'; branch 'master' } }
            steps {
                sh 'echo "push to ECR stage"'
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: "${registryCredential}",
                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY'
                    ]]) {
                        sh """
                        TAG=\$(cat tag.txt)
                        aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin \${registry}
                        docker push 333923656856.dkr.ecr.eu-central-1.amazonaws.com/tasksapp:\$TAG
                         """
                }
                withCredentials([gitUsernamePassword(credentialsId: 'github', gitToolName: 'Default')]) {
                sh """
                    TAG=\$(cat tag.txt)
                    #git config user.email you@example.com
                    #git config user.name kfirosb
                    git tag \$TAG
                    git push --tags
                """
                }
            }
                
        }
    }


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
            deleteDir() //clean up our workspace */

        }
        success {
                updateGitlabCommitStatus name: 'build', state: 'success'

        }
        failure {
                updateGitlabCommitStatus name: 'build', state: 'failed'
        }
    }

}