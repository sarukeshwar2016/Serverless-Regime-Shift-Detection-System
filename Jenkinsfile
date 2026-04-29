pipeline {
    agent any

    environment {
        EC2_HOST = '3.108.178.7'
        EC2_USERNAME = 'ec2-user'
        MONGO_URI = credentials('MONGO_URI')
    }

    stages {
        stage('Fast Deploy (Demo Mode)') {
            steps {
                script {
                    withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                        bat """
                        ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no ${EC2_USERNAME}@${EC2_HOST} "
                        cd Serverless-Regime-Shift-Detection-System &&
                        git fetch origin main &&
                        git reset --hard origin/main &&
                        docker restart regime-platform
                        "
                        """
                    }
                }
            }
        }
    }
}