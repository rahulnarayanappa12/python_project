pipeline {
    agent { label 'label-1' }  // <-- match this to the label set on your agent node

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds-python-project')   // Jenkins credential ID (username + password/token)
        DOCKERHUB_NAMESPACE   = 'rahulnarayanappa'
        IMAGE_NAME            = 'python-project'                          // change to your app name
        IMAGE_TAG              = "${env.BUILD_NUMBER}"
        FULL_IMAGE             = "${DOCKERHUB_NAMESPACE}/${IMAGE_NAME}:${IMAGE_TAG}"

        AWS_REGION   = 'ap-southeast-2'
        CLUSTER_NAME = 'dev-cluster'
        AWS_CREDS    = credentials('aws-eks-creds')
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

       stage('Configure kubeconfig') {
            steps {
                sh '''
                    aws eks update-kubeconfig \
                        --name $CLUSTER_NAME \
                        --region $AWS_REGION
                '''
            }
        }

	stage('Deploy') {
 	   steps {
        	sh '''
            sed -i "s|IMAGE_TAG|$BUILD_NUMBER|g" k8s-files/deployment.yml
            kubectl apply -f k8s-files/deployment.yml
            kubectl apply -f k8s-files/service.yml
            kubectl rollout status deployment/my-deployment --timeout=120s
        '''
   	   }
	}
    }

    post {
        success {
            echo "Deployed ${FULL_IMAGE} successfully."
        }
        failure {
            echo "Pipeline failed. Check logs above."
        }
        always {
			node('label-1') {
            sh 'docker system prune -f || true'
        }
        }
    }
}

