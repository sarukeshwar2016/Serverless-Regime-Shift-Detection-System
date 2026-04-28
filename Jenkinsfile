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
                        sh """
                        ssh -i \${SSH_KEY} -o StrictHostKeyChecking=no ${EC2_USERNAME}@${EC2_HOST} '
                            # 1. Navigate to the project directory
                            cd Serverless-Regime-Shift-Detection-System
                            
                            # 2. Force sync the latest code from GitHub (ignoring local permission changes)
                            git fetch origin main
                            git reset --hard origin/main
                            
                            # 3. Build the Docker image
                            docker build -t regime-platform:latest .
                            
                            # 4. Stop and remove the existing container (if any)
                            docker stop regime-platform || true
                            docker rm regime-platform || true
                            
                            # 5. Run the new container
                            docker run -d \\
                              --name regime-platform \\
                              -p 80:7860 \\
                              -e MONGO_URI="${MONGO_URI}" \\
                              --restart always \\
                              regime-platform:latest
                        '
                        """
                    }
                }
            }
        }
    }
}
