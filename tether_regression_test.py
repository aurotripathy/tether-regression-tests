import docker

# docker paramters
docker_name = 'tt_small'
working_dir='/tenstorrent/releases/tests'
devices = ["/dev/tenstorrent-0"]
cap_add = ['SYS_PTRACE']
security_opt = ["seccomp=unconfined"]
volumes = {'/home/gsworkstationuser01/': {'bind': '/data', 'mode': 'rw'}}

# tether invocations
commands = [{'name': 'sanity',
             'invocation':"tether run --release-mode release --verify none -d grayskull -i sanity.yaml"
             },
           ]

client = docker.from_env()
for container in client.containers.list():
    print('Stopping container', container.id)
    container.stop()
    
for command in commands:
    print('Running command name:', command['name']) 
    print('Running command:', command['invocation']) 
    output = client.containers.run(image="tenstorrent/sw:tt_small",
                                   devices=devices,
                                   cap_add=cap_add,
                                   security_opt=security_opt,
                                   working_dir=working_dir,
                                   stdout=True, stderr=True,
                                   volumes=volumes,
                                   detach=True,
                                   name=docker_name,
                                   remove=True,
                                   command=command['invocation'])
    with open(command['name'] + "-out.txt", 'w')as f:
        f.write('Command used: {}\n'.format(command['invocation']))
        for line in output.logs(stream=True):
            f.write(str(line.strip())+'\n')

