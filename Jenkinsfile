pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'python-webapp'
        DOCKER_TAG = "${BUILD_NUMBER}"
        NEXUS_URL = 'http://master.nexus.local/'
        NEXUS_REPOSITORY = 'docker-hosted'
        NEXUS_CREDENTIAL_ID = 'nexus-credentials'
        GIT_CREDENTIALS_ID = 'git-credentials'
        GIT_REPO_URL = 'https://github.com/adityalaxkar/my-first-app-on-k8s.git'  // Replace with your repo URL
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Push to Nexus') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${NEXUS_CREDENTIAL_ID}", usernameVariable: 'NEXUS_USER', passwordVariable: 'NEXUS_PASS')]) {
                        // Tag image for Nexus
                        sh "docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${NEXUS_URL}/${NEXUS_REPOSITORY}/${DOCKER_IMAGE}:${DOCKER_TAG}"

                        // Login to Nexus
                        sh "echo ${NEXUS_PASS} | docker login ${NEXUS_URL} -u ${NEXUS_USER} --password-stdin"

                        // Push image to Nexus
                        sh "docker push ${NEXUS_URL}/${NEXUS_REPOSITORY}/${DOCKER_IMAGE}:${DOCKER_TAG}"
                    }
                }
            }
        }

        stage('Update Kubernetes Manifests') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${GIT_CREDENTIALS_ID}", usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                        // Configure Git
                        sh """
                            git config user.email "jenkins@example.com"
                            git config user.name "Jenkins"

                            # Update the image tag in the deployment file
                            sed -i 's|image: ${NEXUS_URL}/${NEXUS_REPOSITORY}/${DOCKER_IMAGE}:.*|image: ${NEXUS_URL}/${NEXUS_REPOSITORY}/${DOCKER_IMAGE}:${DOCKER_TAG}|' k8s/applications/python-webapp/deployment.yaml

                            # Commit and push the changes
                            git add k8s/applications/python-webapp/deployment.yaml
                            git commit -m "Update image tag to ${DOCKER_TAG}"
                            git push https://${GIT_USER}:${GIT_PASS}@${GIT_REPO_URL}
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            sh "docker logout ${NEXUS_URL}"
        }
    }
}