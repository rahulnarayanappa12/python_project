pipeline {
    agent label-1  // <-- match this to the label set on your agent node

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds-python-project')   // Jenkins credential ID (username + password/token)
        DOCKERHUB_NAMESPACE   = 'rahulnarayanappa'
        IMAGE_NAME            = 'python-project'                          // change to your app name
        IMAGE_TAG              = "${env.BUILD_NUMBER}"
        FULL_IMAGE             = "${DOCKERHUB_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}"

        // K8S_NAMESPACE           = 'default'                        // change if deploying elsewhere
        // HELM_CHART_PATH          = 'helm-chart'                     // path to chart folder inside the repo
        // HELM_RELEASE_NAME        = 'my-app'                          // helm release name
    }

    options {
        timestamps()   //Adds a timestamp to every line of console output during a build
        buildDiscarder(logRotator(numToKeepStr: '10')) //tells Jenkins: only keep the 10 most recent builds
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                // Pulls whatever repo/branch is configured in the Jenkins job's
                // "Pipeline script from SCM" settings — main.py, requirements.txt,
                // Dockerfile, and helm-chart/ all come from there.
            }
        }

        

        stage('Build Image') {
            steps {
                sh "docker build -t ${FULL_IMAGE} ."
            }
        }

        stage('Push Image') {
            steps {
                sh '''
                    echo "$DOCKERHUB_CREDENTIALS_PSW" | docker login -u "$DOCKERHUB_CREDENTIALS_USR" --password-stdin
                    docker push ${FULL_IMAGE}
                    docker logout
                '''
            }
        }

        /*
        stage('Deploy to Kubernetes (Helm)') {
            when {
                expression { return params.RUN_DEPLOY }
            }
            steps {
                withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG_CREDENTIALS')]) {
                    sh '''
                        export KUBECONFIG=$KUBECONFIG_CREDENTIALS
                        helm upgrade --install ${HELM_RELEASE_NAME} ${HELM_CHART_PATH} \
                            --namespace ${K8S_NAMESPACE} \
                            --set image.repository=${DOCKERHUB_NAMESPACE}/${IMAGE_NAME} \
                            --set image.tag=${IMAGE_TAG} \
                            --wait --timeout 120s
                    '''
                }
            }
        }
        */
    }

    post {
        success {
            echo "Deployed ${FULL_IMAGE} successfully."
        }
        failure {
            echo "Pipeline failed. Check logs above."
        }
        always {
            sh 'docker system prune -f || true'
        }
    }
}

