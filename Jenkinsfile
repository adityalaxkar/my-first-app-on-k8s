pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'python-webapp'
        DOCKER_TAG = "${BUILD_NUMBER}"

    }

    stages {
        stage('checkout') {
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
                    withCredentials([usernamePassword(credentialsId: "$${NEXUS_CREDENTIALS_ID}", usernameVariable: 'NEXUS_USER, passwordVariable: 'NEXUS_PASS')]) {
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
                            git config user.email "jenkins@admin.com"
                            git config user.name "adityal"

                            # update the image tag in the deployment file
                            sed -i 's|image: ${NEXUS_URL}/${NEXUS_REPOSITORY}/${DOCKER_IMAGE}:.*|image: ${NEXUS_URL}/${NEXUS_REPOSITORY}/${DOCKER_IMAGE}:${DOCKER_TAG}|' k8s/applications/python-webapp/deployment.yaml

                            # commit and push the changes
                            git add k8s/applications/python-webapp/deployment.yaml
                            git commit -m "Update image tag to ${DOCKER_TAG}"
                            git push https://${GIT_USER}:${GIT_PASS}@${GIT_REPO_URL#https://}
                        """

                    }
                }
            }
    }

}