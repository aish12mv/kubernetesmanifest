node {
    def app

    stage('Clone repository') {
      

        checkout scm
    }

    stage('Update GIT') {
            script {
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                    withCredentials([usernamePassword(credentialsId: 'github', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
                        //def encodedPassword = URLEncoder.encode("$GIT_PASSWORD",'UTF-8')
                        sh "git config user.email aishwarya.melur@hcl.com"
                        sh "git config user.name aish12mv"
                        //sh "git switch master"
                        sh "cat deployment.yaml"
                        sh "sed -i 's+aishwaryamv/test.*+aishwaryamv/test:${DOCKERTAG}+g' deployment.yaml"
                        sh "cat deployment.yaml"
                        sh "git add ."
                        sh "git commit -m 'Done by Jenkins Job changemanifest: ${env.BUILD_NUMBER}'"
                        sh "git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/${GIT_USERNAME}/kubernetesmanifest.git HEAD:main"
      }
    }
  }
}
     stage('Deploy App to kuberentes') {
      steps {
        script {
          //sh "sed -i s/latest/$BUILD_NUMBER/g $WORKSPACE/deploy.yml"
          kubernetesDeploy configs: 'deployment.yaml', kubeConfig: [path: 'kubernetes_build'], kubeconfigId: 'kubeconfig', secretName: '', ssh: [sshCredentialsId: '*', sshServer: ''], textCredentials: [certificateAuthorityData: '', clientCertificateData: '', clientKeyData: '', serverUrl: 'https://']
        }
      }
    }
}
