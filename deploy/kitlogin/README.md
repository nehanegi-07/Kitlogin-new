
## Docker build, push, and helm install

```
cd /home/mani/sass/kitlogin
source ./kit3.8/bin/activate
Remove existing images:
sudo docker image prune --all
Build image:
sudo docker build -f production.Dockerfile -t kitlogin/kitlogin .
Tag image:
sudo docker tag kitlogin 1007234/kitlogin
Login:
sudo docker login
Push image:
sudo docker push 1007234/kitlogin
Note: 1007234 is the private registry at hub.docker.com.



To create Fargate:
Run following from dir ./kitlogin/deploy
eksctl create cluster -f ./kitlogin/fg.yaml
eksctl delete cluster --name kitlogin-prod


Helm install: 
helm install [RELEASE_NAME] [CHART_NAME] --values [VALUES_FILE]
To install the apps and automatically create an ELB and associate it with Nginx and *.analyticlit.com certificate:
Run following from dir ./kitlogin/deploy
helm install kitlogin ./kitlogin --values ./kitlogin/values.yaml --create-namespace --debug (1st time)
helm upgrade kitlogin ./kitlogin --values ./kitlogin/values.yaml --debug (2nd time onwards)
helm delete kitlogin (delete app )



To create a CNAME record in Cloudflare:
Setup Cloudflare
1. Get the DNS name (A record) from AWS ELB a04a6691a240b439f8c7e517887962f4-956770048.us-east-1.elb.amazonaws.com.
2. Create a CNAME record in Cloudflare with the above AWS ELB.
3. Set the "Proxied" option in Cloudflare.


====================================================
helm install output
Release "kitlogin" has been upgraded. Happy Helming!
NAME: kitlogin
LAST DEPLOYED: Sun May 28 17:33:24 2023
NAMESPACE: default
STATUS: deployed
REVISION: 6
TEST SUITE: None
USER-SUPPLIED VALUES:
cert-manager:
  email: analytickit@gmail.com
  enabled: false
  installCRDs: true
  podDnsConfig:
    nameservers:
    - 8.8.8.8
    - 1.1.1.1
    - 208.67.222.222
  podDnsPolicy: None
cloud: aws
cloudwatch:
  clusterName: null
  enabled: false
  fluentBit:
    port: 2020
    readHead: "On"
    readTail: "Off"
    server: "On"
  region: null
email:
  existingSecret: ""
  existingSecretKey: ""
  from_email: null
  host: null
  password: null
  port: null
  use_ssl: null
  use_tls: true
  user: null
env: []
externalObjectStorage:
  bucket: null
  endpoint: null
  existingSecret: null
  host: null
  port: null
hooks:
  affinity: {}
  migrate:
    env: []
    resources: {}
  nodeSelector: {}
  tolerations: []
image:
  default: :latest
  pullPolicy: Always
  repository: 1007234/kitlogin
  sha: null
  tag: null
ingress:
  annotations: {}
  enabled: true
  gcp:
    forceHttps: true
    ip_name: kitlogin
    secretName: ""
  hostname: sca.analytickit.com
  letsencrypt: null
  nginx:
    enabled: true
    redirectToTLS: true
  secretName: null
  tolerations:
  - effect: NoSchedule
    key: eks.amazonaws.com/compute-type
    operator: Equal
    value: fargate
  type: null
ingress-nginx:
  controller:
    config:
      log-format-escape-json: "true"
      log-format-upstream: '{ "time": "$time_iso8601", "remote_addr": "$proxy_protocol_addr",
        "request_id": "$request_id", "correlation_id": "$request_id", "remote_user":
        "$remote_user", "bytes_sent": $bytes_sent, "request_time": $request_time,
        "status": $status, "host": "$host", "request_proto": "$server_protocol", "uri":
        "$uri", "request_query": "$args", "request_length": $request_length, "duration":
        $request_time, "method": "$request_method", "http_referrer": "$http_referer",
        "http_user_agent": "$http_user_agent", "http_x_forwarded_for": "$http_x_forwarded_for"
        }'
      proxy_ssl_server_name: "on"
      use-forwarded-headers: "true"
    proxySetHeaders:
      X-Correlation-ID: $request_id
kitloginSecretKey:
  existingSecret: null
  existingSecretKey: kitlogin-secret
notificationEmail: analytickit@gmail.com
saml:
  acs_url: null
  attr_email: null
  attr_first_name: null
  attr_last_name: null
  attr_permanent_id: null
  disabled: false
  enforced: false
  entity_id: null
  x509_cert: null
sentryDSN: null
service:
  annotations: {}
  externalPort: 8083
  internalPort: 3000
  name: kitlogin
  type: NodePort
serviceAccount:
  annotations: {}
  create: true
  name: null
siteUrl: https://sca.analytickit.com

COMPUTED VALUES:
cert-manager:
  email: analytickit@gmail.com
  enabled: false
  installCRDs: true
  podDnsConfig:
    nameservers:
    - 8.8.8.8
    - 1.1.1.1
    - 208.67.222.222
  podDnsPolicy: None
cloud: aws
cloudwatch:
  enabled: false
  fluentBit:
    port: 2020
    readHead: "On"
    readTail: "Off"
    server: "On"
email:
  existingSecret: ""
  existingSecretKey: ""
  use_tls: true
env: []
externalObjectStorage: {}
hooks:
  affinity: {}
  migrate:
    env: []
    resources: {}
  nodeSelector: {}
  tolerations: []
image:
  default: :latest
  pullPolicy: Always
  repository: 1007234/kitlogin
ingress:
  annotations: {}
  enabled: true
  gcp:
    forceHttps: true
    ip_name: kitlogin
    secretName: ""
  hostname: sca.analytickit.com
  nginx:
    enabled: true
    redirectToTLS: true
  tolerations:
  - effect: NoSchedule
    key: eks.amazonaws.com/compute-type
    operator: Equal
    value: fargate
ingress-nginx:
  controller:
    addHeaders: {}
    admissionWebhooks:
      annotations: {}
      certificate: /usr/local/certificates/cert
      createSecretJob:
        resources: {}
      enabled: true
      existingPsp: ""
      failurePolicy: Fail
      key: /usr/local/certificates/key
      labels: {}
      namespaceSelector: {}
      objectSelector: {}
      patch:
        enabled: true
        image:
          digest: sha256:64d8c73dca984af206adf9d6d7e46aa550362b1d7a01f3a0a91b20cc67868660
          image: ingress-nginx/kube-webhook-certgen
          pullPolicy: IfNotPresent
          registry: k8s.gcr.io
          tag: v1.1.1
        labels: {}
        nodeSelector:
          kubernetes.io/os: linux
        podAnnotations: {}
        priorityClassName: ""
        runAsUser: 2000
        tolerations: []
      patchWebhookJob:
        resources: {}
      port: 8443
      service:
        annotations: {}
        externalIPs: []
        loadBalancerSourceRanges: []
        servicePort: 443
        type: ClusterIP
    affinity: {}
    allowSnippetAnnotations: true
    annotations: {}
    autoscaling:
      behavior: {}
      enabled: false
      maxReplicas: 11
      minReplicas: 1
      targetCPUUtilizationPercentage: 50
      targetMemoryUtilizationPercentage: 50
    autoscalingTemplate: []
    config:
      log-format-escape-json: "true"
      log-format-upstream: '{ "time": "$time_iso8601", "remote_addr": "$proxy_protocol_addr",
        "request_id": "$request_id", "correlation_id": "$request_id", "remote_user":
        "$remote_user", "bytes_sent": $bytes_sent, "request_time": $request_time,
        "status": $status, "host": "$host", "request_proto": "$server_protocol", "uri":
        "$uri", "request_query": "$args", "request_length": $request_length, "duration":
        $request_time, "method": "$request_method", "http_referrer": "$http_referer",
        "http_user_agent": "$http_user_agent", "http_x_forwarded_for": "$http_x_forwarded_for"
        }'
      proxy_ssl_server_name: "on"
      use-forwarded-headers: "true"
    configAnnotations: {}
    configMapNamespace: ""
    containerName: controller
    containerPort:
      http: 80
      https: 443
    customTemplate:
      configMapKey: ""
      configMapName: ""
    dnsConfig: {}
    dnsPolicy: ClusterFirst
    electionID: ingress-controller-leader
    enableMimalloc: true
    existingPsp: ""
    extraArgs: {}
    extraContainers: []
    extraEnvs: []
    extraInitContainers: []
    extraVolumeMounts: []
    extraVolumes: []
    healthCheckHost: ""
    healthCheckPath: /healthz
    hostNetwork: false
    hostPort:
      enabled: false
      ports:
        http: 80
        https: 443
    hostname: {}
    image:
      allowPrivilegeEscalation: true
      digest: sha256:f766669fdcf3dc26347ed273a55e754b427eb4411ee075a53f30718b4499076a
      image: ingress-nginx/controller
      pullPolicy: IfNotPresent
      registry: k8s.gcr.io
      runAsUser: 101
      tag: v1.1.0
    ingressClassByName: false
    ingressClassResource:
      controllerValue: k8s.io/ingress-nginx
      default: false
      enabled: true
      name: nginx
      parameters: {}
    keda:
      apiVersion: keda.sh/v1alpha1
      behavior: {}
      cooldownPeriod: 300
      enabled: false
      maxReplicas: 11
      minReplicas: 1
      pollingInterval: 30
      restoreToOriginalReplicaCount: false
      scaledObject:
        annotations: {}
      triggers: []
    kind: Deployment
    labels: {}
    lifecycle:
      preStop:
        exec:
          command:
          - /wait-shutdown
    livenessProbe:
      failureThreshold: 5
      httpGet:
        path: /healthz
        port: 10254
        scheme: HTTP
      initialDelaySeconds: 10
      periodSeconds: 10
      successThreshold: 1
      timeoutSeconds: 1
    maxmindLicenseKey: ""
    metrics:
      enabled: false
      port: 10254
      prometheusRule:
        additionalLabels: {}
        enabled: false
        rules: []
      service:
        annotations: {}
        externalIPs: []
        loadBalancerSourceRanges: []
        servicePort: 10254
        type: ClusterIP
      serviceMonitor:
        additionalLabels: {}
        enabled: false
        metricRelabelings: []
        namespace: ""
        namespaceSelector: {}
        relabelings: []
        scrapeInterval: 30s
        targetLabels: []
    minAvailable: 1
    minReadySeconds: 0
    name: controller
    nodeSelector:
      kubernetes.io/os: linux
    podAnnotations: {}
    podLabels: {}
    podSecurityContext: {}
    priorityClassName: ""
    proxySetHeaders:
      X-Correlation-ID: $request_id
    publishService:
      enabled: true
      pathOverride: ""
    readinessProbe:
      failureThreshold: 3
      httpGet:
        path: /healthz
        port: 10254
        scheme: HTTP
      initialDelaySeconds: 10
      periodSeconds: 10
      successThreshold: 1
      timeoutSeconds: 1
    replicaCount: 1
    reportNodeInternalIp: false
    resources:
      requests:
        cpu: 100m
        memory: 90Mi
    scope:
      enabled: false
      namespace: ""
      namespaceSelector: ""
    service:
      annotations: {}
      appProtocol: true
      enableHttp: true
      enableHttps: true
      enabled: true
      external:
        enabled: true
      externalIPs: []
      internal:
        annotations: {}
        enabled: false
        loadBalancerSourceRanges: []
      ipFamilies:
      - IPv4
      ipFamilyPolicy: SingleStack
      labels: {}
      loadBalancerSourceRanges: []
      nodePorts:
        http: ""
        https: ""
        tcp: {}
        udp: {}
      ports:
        http: 80
        https: 443
      targetPorts:
        http: http
        https: https
      type: LoadBalancer
    sysctls: {}
    tcp:
      annotations: {}
      configMapNamespace: ""
    terminationGracePeriodSeconds: 300
    tolerations: []
    topologySpreadConstraints: []
    udp:
      annotations: {}
      configMapNamespace: ""
    updateStrategy: {}
    watchIngressWithoutClass: false
  defaultBackend:
    affinity: {}
    autoscaling:
      annotations: {}
      enabled: false
      maxReplicas: 2
      minReplicas: 1
      targetCPUUtilizationPercentage: 50
      targetMemoryUtilizationPercentage: 50
    containerSecurityContext: {}
    enabled: false
    existingPsp: ""
    extraArgs: {}
    extraEnvs: []
    extraVolumeMounts: []
    extraVolumes: []
    image:
      allowPrivilegeEscalation: false
      image: defaultbackend-amd64
      pullPolicy: IfNotPresent
      readOnlyRootFilesystem: true
      registry: k8s.gcr.io
      runAsNonRoot: true
      runAsUser: 65534
      tag: "1.5"
    labels: {}
    livenessProbe:
      failureThreshold: 3
      initialDelaySeconds: 30
      periodSeconds: 10
      successThreshold: 1
      timeoutSeconds: 5
    minAvailable: 1
    name: defaultbackend
    nodeSelector:
      kubernetes.io/os: linux
    podAnnotations: {}
    podLabels: {}
    podSecurityContext: {}
    port: 8080
    priorityClassName: ""
    readinessProbe:
      failureThreshold: 6
      initialDelaySeconds: 0
      periodSeconds: 5
      successThreshold: 1
      timeoutSeconds: 5
    replicaCount: 1
    resources: {}
    service:
      annotations: {}
      externalIPs: []
      loadBalancerSourceRanges: []
      servicePort: 80
      type: ClusterIP
    serviceAccount:
      automountServiceAccountToken: true
      create: true
      name: ""
    tolerations: []
  global: {}
  imagePullSecrets: []
  podSecurityPolicy:
    enabled: false
  rbac:
    create: true
    scope: false
  revisionHistoryLimit: 10
  serviceAccount:
    automountServiceAccountToken: true
    create: true
    name: ""
  tcp: {}
  udp: {}
kitloginSecretKey:
  existingSecretKey: kitlogin-secret
notificationEmail: analytickit@gmail.com
saml:
  disabled: false
  enforced: false
service:
  annotations: {}
  externalPort: 8083
  internalPort: 3000
  name: kitlogin
  type: NodePort
serviceAccount:
  annotations: {}
  create: true
siteUrl: https://sca.analytickit.com

HOOKS:
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/admission-webhooks/job-patch/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: kitlogin-ingress-nginx-admission
  namespace: default
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade,post-install,post-upgrade
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/admission-webhooks/job-patch/clusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: kitlogin-ingress-nginx-admission
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade,post-install,post-upgrade
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
rules:
  - apiGroups:
      - admissionregistration.k8s.io
    resources:
      - validatingwebhookconfigurations
    verbs:
      - get
      - update
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/admission-webhooks/job-patch/clusterrolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name:  kitlogin-ingress-nginx-admission
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade,post-install,post-upgrade
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kitlogin-ingress-nginx-admission
subjects:
  - kind: ServiceAccount
    name: kitlogin-ingress-nginx-admission
    namespace: "default"
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/admission-webhooks/job-patch/role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name:  kitlogin-ingress-nginx-admission
  namespace: default
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade,post-install,post-upgrade
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
rules:
  - apiGroups:
      - ""
    resources:
      - secrets
    verbs:
      - get
      - create
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/admission-webhooks/job-patch/rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: kitlogin-ingress-nginx-admission
  namespace: default
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade,post-install,post-upgrade
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: kitlogin-ingress-nginx-admission
subjects:
  - kind: ServiceAccount
    name: kitlogin-ingress-nginx-admission
    namespace: "default"
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/admission-webhooks/job-patch/job-createSecret.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: kitlogin-ingress-nginx-admission-create
  namespace: default
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
spec:
  template:
    metadata:
      name: kitlogin-ingress-nginx-admission-create
      labels:
        helm.sh/chart: ingress-nginx-4.0.13
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/instance: kitlogin
        app.kubernetes.io/version: "1.1.0"
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/component: admission-webhook
    spec:
      containers:
        - name: create
          image: "k8s.gcr.io/ingress-nginx/kube-webhook-certgen:v1.1.1@sha256:64d8c73dca984af206adf9d6d7e46aa550362b1d7a01f3a0a91b20cc67868660"
          imagePullPolicy: IfNotPresent
          args:
            - create
            - --host=kitlogin-ingress-nginx-controller-admission,kitlogin-ingress-nginx-controller-admission.$(POD_NAMESPACE).svc
            - --namespace=$(POD_NAMESPACE)
            - --secret-name=kitlogin-ingress-nginx-admission
          env:
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          securityContext:
            allowPrivilegeEscalation: false
      restartPolicy: OnFailure
      serviceAccountName: kitlogin-ingress-nginx-admission
      nodeSelector: 
        kubernetes.io/os: linux
      securityContext:
        runAsNonRoot: true
        runAsUser: 2000
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/admission-webhooks/job-patch/job-patchWebhook.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: kitlogin-ingress-nginx-admission-patch
  namespace: default
  annotations:
    "helm.sh/hook": post-install,post-upgrade
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
spec:
  template:
    metadata:
      name: kitlogin-ingress-nginx-admission-patch
      labels:
        helm.sh/chart: ingress-nginx-4.0.13
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/instance: kitlogin
        app.kubernetes.io/version: "1.1.0"
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/component: admission-webhook
    spec:
      containers:
        - name: patch
          image: "k8s.gcr.io/ingress-nginx/kube-webhook-certgen:v1.1.1@sha256:64d8c73dca984af206adf9d6d7e46aa550362b1d7a01f3a0a91b20cc67868660"
          imagePullPolicy: IfNotPresent
          args:
            - patch
            - --webhook-name=kitlogin-ingress-nginx-admission
            - --namespace=$(POD_NAMESPACE)
            - --patch-mutating=false
            - --secret-name=kitlogin-ingress-nginx-admission
            - --patch-failure-policy=Fail
          env:
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          securityContext:
            allowPrivilegeEscalation: false
      restartPolicy: OnFailure
      serviceAccountName: kitlogin-ingress-nginx-admission
      nodeSelector: 
        kubernetes.io/os: linux
      securityContext:
        runAsNonRoot: true
        runAsUser: 2000
MANIFEST:
---
# Source: kitlogin-chart/templates/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: kitlogin
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/controller-serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: kitlogin-ingress-nginx
  namespace: default
automountServiceAccountToken: true
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/controller-configmap-proxyheaders.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: kitlogin-ingress-nginx-custom-proxy-headers
  namespace: default
data:
  X-Correlation-ID: $request_id
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/controller-configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: kitlogin-ingress-nginx-controller
  namespace: default
data:
  allow-snippet-annotations: "true"
  proxy-set-headers: default/kitlogin-ingress-nginx-custom-proxy-headers
  log-format-escape-json: "true"
  log-format-upstream: "{ \"time\": \"$time_iso8601\", \"remote_addr\": \"$proxy_protocol_addr\", \"request_id\": \"$request_id\", \"correlation_id\": \"$request_id\", \"remote_user\": \"$remote_user\", \"bytes_sent\": $bytes_sent, \"request_time\": $request_time, \"status\": $status, \"host\": \"$host\", \"request_proto\": \"$server_protocol\", \"uri\": \"$uri\", \"request_query\": \"$args\", \"request_length\": $request_length, \"duration\": $request_time, \"method\": \"$request_method\", \"http_referrer\": \"$http_referer\", \"http_user_agent\": \"$http_user_agent\", \"http_x_forwarded_for\": \"$http_x_forwarded_for\" }"
  proxy_ssl_server_name: "on"
  use-forwarded-headers: "true"
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/clusterrole.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
  name: kitlogin-ingress-nginx
rules:
  - apiGroups:
      - ""
    resources:
      - configmaps
      - endpoints
      - nodes
      - pods
      - secrets
      - namespaces
    verbs:
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - nodes
    verbs:
      - get
  - apiGroups:
      - ""
    resources:
      - services
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingresses
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - events
    verbs:
      - create
      - patch
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingresses/status
    verbs:
      - update
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingressclasses
    verbs:
      - get
      - list
      - watch
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/clusterrolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
  name: kitlogin-ingress-nginx
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: kitlogin-ingress-nginx
subjects:
  - kind: ServiceAccount
    name: kitlogin-ingress-nginx
    namespace: "default"
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/controller-role.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: kitlogin-ingress-nginx
  namespace: default
rules:
  - apiGroups:
      - ""
    resources:
      - namespaces
    verbs:
      - get
  - apiGroups:
      - ""
    resources:
      - configmaps
      - pods
      - secrets
      - endpoints
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - services
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingresses
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingresses/status
    verbs:
      - update
  - apiGroups:
      - networking.k8s.io
    resources:
      - ingressclasses
    verbs:
      - get
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - configmaps
    resourceNames:
      - ingress-controller-leader
    verbs:
      - get
      - update
  - apiGroups:
      - ""
    resources:
      - configmaps
    verbs:
      - create
  - apiGroups:
      - ""
    resources:
      - events
    verbs:
      - create
      - patch
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/controller-rolebinding.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: kitlogin-ingress-nginx
  namespace: default
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: kitlogin-ingress-nginx
subjects:
  - kind: ServiceAccount
    name: kitlogin-ingress-nginx
    namespace: "default"
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/controller-service-webhook.yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: kitlogin-ingress-nginx-controller-admission
  namespace: default
spec:
  type: ClusterIP
  ports:
    - name: https-webhook
      port: 443
      targetPort: webhook
  selector:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/component: controller
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/controller-service.yaml
apiVersion: v1
kind: Service
metadata:
  annotations:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: kitlogin-ingress-nginx-controller
  namespace: default
spec:
  type: LoadBalancer
  ipFamilyPolicy: SingleStack
  ipFamilies: 
    - IPv4
  ports:
    - name: http
      port: 80
      protocol: TCP
      targetPort: http
    - name: https
      port: 443
      protocol: TCP
      targetPort: https
  selector:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/component: controller
---
# Source: kitlogin-chart/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: kitlogin-kitlogin-chart-app
  labels:
    
    "helm.sh/chart": "kitlogin-chart-1.0.0"
  annotations:
    
    "meta.helm.sh/release-name": "kitlogin"
    "meta.helm.sh/release-namespace": "default"
spec:
  type: NodePort
  ports:
  - port: 8083
    targetPort: 3000
    protocol: TCP
    name: kitlogin
  selector:
    app: kitlogin-kitlogin-chart
    role: web
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/controller-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: kitlogin-ingress-nginx-controller
  namespace: default
spec:
  selector:
    matchLabels:
      app.kubernetes.io/name: ingress-nginx
      app.kubernetes.io/instance: kitlogin
      app.kubernetes.io/component: controller
  replicas: 1
  revisionHistoryLimit: 10
  minReadySeconds: 0
  template:
    metadata:
      labels:
        app.kubernetes.io/name: ingress-nginx
        app.kubernetes.io/instance: kitlogin
        app.kubernetes.io/component: controller
    spec:
      dnsPolicy: ClusterFirst
      containers:
        - name: controller
          image: "k8s.gcr.io/ingress-nginx/controller:v1.1.0@sha256:f766669fdcf3dc26347ed273a55e754b427eb4411ee075a53f30718b4499076a"
          imagePullPolicy: IfNotPresent
          lifecycle: 
            preStop:
              exec:
                command:
                - /wait-shutdown
          args:
            - /nginx-ingress-controller
            - --publish-service=$(POD_NAMESPACE)/kitlogin-ingress-nginx-controller
            - --election-id=ingress-controller-leader
            - --controller-class=k8s.io/ingress-nginx
            - --configmap=$(POD_NAMESPACE)/kitlogin-ingress-nginx-controller
            - --validating-webhook=:8443
            - --validating-webhook-certificate=/usr/local/certificates/cert
            - --validating-webhook-key=/usr/local/certificates/key
          securityContext: 
            capabilities:
              drop:
              - ALL
              add:
              - NET_BIND_SERVICE
            runAsUser: 101
            allowPrivilegeEscalation: true
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: LD_PRELOAD
              value: /usr/local/lib/libmimalloc.so
          livenessProbe: 
            failureThreshold: 5
            httpGet:
              path: /healthz
              port: 10254
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 1
          readinessProbe: 
            failureThreshold: 3
            httpGet:
              path: /healthz
              port: 10254
              scheme: HTTP
            initialDelaySeconds: 10
            periodSeconds: 10
            successThreshold: 1
            timeoutSeconds: 1
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
            - name: https
              containerPort: 443
              protocol: TCP
            - name: webhook
              containerPort: 8443
              protocol: TCP
          volumeMounts:
            - name: webhook-cert
              mountPath: /usr/local/certificates/
              readOnly: true
          resources: 
            requests:
              cpu: 100m
              memory: 90Mi
      nodeSelector: 
        kubernetes.io/os: linux
      serviceAccountName: kitlogin-ingress-nginx
      terminationGracePeriodSeconds: 300
      volumes:
        - name: webhook-cert
          secret:
            secretName: kitlogin-ingress-nginx-admission
---
# Source: kitlogin-chart/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kitlogin-apps-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kitlogin-apps
  template:
    metadata:
      labels:
        app: kitlogin-apps
    spec:
      containers:
        - name: kitlogin-chart-app
          image: "1007234/kitlogin:latest"
          imagePullPolicy: Always
          ports:
            - containerPort: 3000
          env:
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/controller-ingressclass.yaml
# We don't support namespaced ingressClass yet
# So a ClusterRole and a ClusterRoleBinding is required
apiVersion: networking.k8s.io/v1
kind: IngressClass
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: controller
  name: nginx
spec:
  controller: k8s.io/ingress-nginx
---
# Source: kitlogin-chart/templates/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: kitlogin-kitlogin-chart
  labels:
    
    "helm.sh/chart": "kitlogin-chart-1.0.0"
  annotations:
    
    "meta.helm.sh/release-name": "kitlogin"
    "meta.helm.sh/release-namespace": "default"
    kubernetes.io/ingress.class: "nginx"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
spec:
  rules:
    - host: sca.analytickit.com
      http:
        paths:
          - pathType: Prefix
            path: "/"
            backend:
              service:
                name: kitlogin-kitlogin-chart-app
                port:
                  number: 8083
---
# Source: kitlogin-chart/charts/ingress-nginx/templates/admission-webhooks/validating-webhook.yaml
# before changing this value, check the required kubernetes version
# https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#prerequisites
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  labels:
    helm.sh/chart: ingress-nginx-4.0.13
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: kitlogin
    app.kubernetes.io/version: "1.1.0"
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/component: admission-webhook
  name: kitlogin-ingress-nginx-admission
webhooks:
  - name: validate.nginx.ingress.kubernetes.io
    matchPolicy: Equivalent
    rules:
      - apiGroups:
          - networking.k8s.io
        apiVersions:
          - v1
        operations:
          - CREATE
          - UPDATE
        resources:
          - ingresses
    failurePolicy: Fail
    sideEffects: None
    admissionReviewVersions:
      - v1
    clientConfig:
      service:
        namespace: "default"
        name: kitlogin-ingress-nginx-controller-admission
        path: /networking/v1/ingresses
