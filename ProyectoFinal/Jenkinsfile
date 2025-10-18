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
    }

    post {
        success { echo "✅ Pipeline completado con éxito" }
        failure { echo "❌ Error en alguna etapa del pipeline" }
        }
}
