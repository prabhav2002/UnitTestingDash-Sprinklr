pipeline {
  agent any
  stages {
    stage('DockerCompose') {
      steps {
        sh "docker-compose build"
        sh "docker-compose up -d"
      }
    }
  }
  post {
    always {
      sh 'docker-compose down --remove-orphans -v'
      sh 'docker-compose ps'
    }
  }
}