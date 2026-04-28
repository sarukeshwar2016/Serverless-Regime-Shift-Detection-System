pipeline {
    agent any

    environment {
        // EC2 Credentials and Host details
        EC2_HOST = '52.66.244.207'
        EC2_USERNAME = 'ec2-user'
        
        // Load MongoDB URI from Jenkins Credentials (Secret text type with ID 'MONGO_URI')
        MONGO_URI = credentials('MONGO_URI')
    }

    stages {
        stage('Deploy to EC2') {
            steps {
                script {
                    // Use standard withCredentials instead of sshagent plugin
                    withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                        bat """
                        ssh -i "%SSH_KEY%" -o StrictHostKeyChecking=no ${EC2_USERNAME}@${EC2_HOST} "cd Serverless-Regime-Shift-Detection-System && git fetch origin main && git reset --hard origin/main && docker build -t regime-platform:latest . && docker stop regime-platform || true && docker rm regime-platform || true && docker run -d --name regime-platform -p 80:7860 -e MONGO_URI='${MONGO_URI}' --restart always regime-platform:latest"
                        """
                    }
                }
            }
        }
    }
}
