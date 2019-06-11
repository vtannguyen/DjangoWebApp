pipeline {
	agent none
	stages {
		stage('Build') {
			steps {
				sh 'cd src/'
				sh 'docker build -t web -f docker-compose.yml .'
			}
		}
	}
}
