pipeline {
        agent any

        stages {
                stage('Preparar entorno') {
            steps {
                echo "Creando entorno virtual..."
                bat '"C:\\Users\\nilto\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m venv venv'
                bat 'venv\\Scripts\\activate && pip install -r requirements.txt'
            }
        }

        stage('Ejecutar script') {
            steps {
            echo "Ejecutando script principal..."
            bat 'venv\\Scripts\\activate && python ETL_VENTAS.py'
            }
        }
        stage('Archivar: Guardar los Resultados') {
            steps {
                // Guarda los archivos generados como "artefactos" del build
                archiveArtifacts artifacts: '*.png, *.csv', allowEmptyArchive: true
            }
        }
    }

    post {
        success { echo "✅ Pipeline completado con éxito" }
        failure {// --- AÑADE ESTO ---
        emailext (
            to: 'niltonbc10@gmail.com', // El correo donde recibirás la alerta
            subject: "FALLO en el Pipeline: ${env.JOB_NAME} [Build #${env.BUILD_NUMBER}]",
            body: """<p>La ejecución #${env.BUILD_NUMBER} del pipeline '${env.JOB_NAME}' ha fallado.</p>
                     <p><b>Estado del Build:</b> ${currentBuild.currentResult}</p>
                     <p><b>Causa del error:</b> Revisa la salida de la consola para más detalles.</p>
                     <p><b>Aquí está el enlace directo a la ejecución:</b></br>
                     <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>"""
        )
        // --- FIN DE LA SECCIÓN AÑADIDA --- 
        }
        always {
        // Limpia el espacio de trabajo para la siguiente ejecución
        cleanWs()
    }
}
}
