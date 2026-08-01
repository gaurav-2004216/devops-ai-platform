pipeline {
agent any


environment {
    IMAGE_NAME = "gaurav262004/ai-devsecops-backend"
    IMAGE_TAG = "${BUILD_NUMBER}"
    DOCKER_CREDENTIALS = "dockerhub-creds"
}

stages {

    stage('Checkout Source') {
        steps {
            checkout scm
        }
    }

    stage('Show Workspace') {
        steps {
            sh 'pwd'
            sh 'ls -R'
        }
    }

    stage('Gitleaks Scan') {
        steps {
            sh '''
            gitleaks detect \
            --source . \
            --report-format json \
            --report-path gitleaks-report.json || true
            '''
        }
    }

    stage('Trivy Filesystem Scan') {
        steps {
            sh '''
            trivy fs . \
            --format table \
            --output trivy-fs-report.txt || true
            '''
        }
    }

   stage('SonarQube Scan') {
    steps {

        withCredentials([string(
            credentialsId: 'sonarqube-token',
            variable: 'SONAR_TOKEN'
        )]) {

            sh '''
            echo "Running SonarQube Scan"

            sonar-scanner \
            -Dsonar.projectKey=DevSecOps \
            -Dsonar.sources=. \
            -Dsonar.host.url=http://localhost:9000 \
            -Dsonar.login=$SONAR_TOKEN
            '''
        }
    }
}

    stage('Build Docker Image') {
        steps {
            sh '''
            docker build \
            -t $IMAGE_NAME:$IMAGE_TAG \
            -f app/backend/Dockerfile .
            '''
        }
    }

    stage('Trivy Image Scan') {
        steps {
            sh '''
            trivy image \
            $IMAGE_NAME:$IMAGE_TAG \
            --format table \
            --output trivy-image-report.txt || true
            '''
        }
    }

    stage('Push Docker Image') {
        steps {
            withCredentials([usernamePassword(
                credentialsId: 'dockerhub-creds',
                usernameVariable: 'DOCKER_USER',
                passwordVariable: 'DOCKER_PASS'
            )]) {

                sh '''
                echo $DOCKER_PASS | docker login \
                -u $DOCKER_USER \
                --password-stdin

                docker push $IMAGE_NAME:$IMAGE_TAG
                '''
            }
        }
    }

    stage('Deploy to Kubernetes') {
        steps {
            sh '''
            kubectl apply -f kubernetes/
            '''
        }
    }

    stage('Verify Deployment') {
        steps {
            sh '''
            kubectl get pods
            kubectl get svc
            '''
        }
    }

}

post {

    always {

        archiveArtifacts artifacts: '*.json', allowEmptyArchive: true

        archiveArtifacts artifacts: '*.txt', allowEmptyArchive: true

        cleanWs()

    }

    success {
        echo "Pipeline Completed Successfully"
    }

    failure {
        echo "Pipeline Failed"
    }

}


}

