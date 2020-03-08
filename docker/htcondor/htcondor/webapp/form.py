from flask import Flask, request, render_template
import os
import subprocess
import logging
from wtforms import Form, StringField, PasswordField, validators

APP = Flask(__name__)


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    token = PasswordField('IAM-Access-Token', [validators.DataRequired()])


@APP.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate():
        print(form.username.data,
              form.token.data)

        # RUN GO COMMAND AND GET OUTPUT
        #
        command = "tts-cache --config /app/.config.yaml --map-user --user {} --token {}".format(
            form.username.data, form.token.data)

        get_DN = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

        DN, err = get_DN.communicate()
        logging.info("Command output: %s error: %s", DN, err)

        # 2020/02/06 11:05:29 UserDN: /C=IT/O=CLOUD@CNAF/CN=1e7074e5-96fe-43e8-881d-4d572c128931@dodas-iam
        try:
            DN = err.split("UserDN: ")[1].replace("/", "\/").rstrip()
        except Exception as ex:
            logging.error("failed to get dn from:  %s",
                          form.username.data, ex)
            return render_template('register.html', DN, form=form)

        with open('/home/uwdir/condormapfile', 'r') as condor_file:
            old = condor_file.read()
            with open('/home/uwdir/temp_file', 'w') as temp_file:
                entry = "GSI \"^" + DN + "$\"  " + form.username.data + " \n"
                temp_file.write(entry)
                temp_file.write(old)
        os.rename('/home/uwdir/temp_file', '/home/uwdir/condormapfile')

        command = "adduser {}".format(form.username.data)

        create_user = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

        _, err = create_user.communicate()

        if err:
            logging.error("failed to add user %s: %s", form.username.data, err)
        else:
            logging.info("Created user %s", form.username.data)

        # condor_reconfig

        command = "condor_reconfig"

        condor_reconfig = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )

        _, err = condor_reconfig.communicate()

        if err:
            logging.error("failed to reconfig condor: %s", err)
        else:
            logging.info("Condor schedd reconfigured")

            return render_template('success.html')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    logging.basicConfig(filename='/var/log/form/app.log',
                        format='[%(asctime)s][%(levelname)s][%(filename)s@%(lineno)d]->[%(message)s]',
                        level=logging.DEBUG)
    APP.logger.setLevel(logging.DEBUG)
    # TODO: if env PORT, otherwise 8080
    port = os.getenv('WEBUI_PORT', default='48080')
    APP.run(host="0.0.0.0", port=int(port))
