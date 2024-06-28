# Conexión de Botpress a WhatsApp
Puedes consultar este video de Botpress para ver un tutorial en video de los siguientes pasos. Si nunca has usado WhatsApp para empresas, consulta esta página. Este tutorial usará un número de prueba de WhatsApp que se creará automáticamente para ti. Creo que no puedes tener dos números de prueba bajo una cuenta comercial de Meta.

Pasos
1. Crea un bot en Botpress

2. Asegúrate de que el bot esté publicado

3. Ve a tu cuenta de Meta Developers

4. Crea una aplicación, otra, empresa, nombra tu aplicación, selecciona WhatsApp como la integración

5. En Botpress, ve a integración y haz clic en "Examinar en el centro"

6. Selecciona WhatsApp e instálalo en tu proyecto de Botpress

7. Ahora tienes que completar el token de verificación, el token de acceso y el número predeterminado

   - Token de verificación: una cadena que puedes seleccionar (por ejemplo, 12345)

   - Token de acceso: en el panel de la aplicación Meta, ve a Configuración de API y copia tu token de acceso temporal (válido por 24 horas)

   - Número predeterminado: en la página de configuración de API, también puedes copiar el ID del número de teléfono para tu número de prueba

1. Presiona guardar y habilita la integración

2. Ahora, en la misma página, copia la URL de webhook de la página de integración de WhatsApp de Botpress

3. Regresa a tu aplicación Meta, selecciona Configuración y edita la URL de devolución de llamada

4. Pega la URL de webhook y tu mismo token de verificación que acabas de crear (por ejemplo, nuevamente, 12345)

5. Ahora haz clic en verificar y guardar

6. Ahora, en la misma página, ve a campos de webhook, administra y suscríbete a mensajes

7. Ahora regresa a Configuración de API y selecciona tu número de teléfono de prueba (o agrégalo si es la primera vez). Este debe ser tu propio número al que tienes acceso.

8. A continuación, haz clic en enviar mensaje de prueba y espera a que tu mensaje aparezca en WhatsApp (esto puede tardar de 60 a 120 segundos).

9. Tu conexión con Botpress ahora debería estar activa y puedes comenzar a chatear.
