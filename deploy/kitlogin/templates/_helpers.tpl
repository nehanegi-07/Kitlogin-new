{{/* vim: set filetype=mustache: */}}

{{/*
Expand the name of the chart.
*/}}
{{- define "kitlogin.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "kitlogin.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}



{{/*
Set the kitlogin image
*/}}
{{- define "kitlogin.image.fullPath" -}}
{{ if .Values.image.sha -}}
"{{ .Values.image.repository }}@{{ .Values.image.sha }}"
{{- else if .Values.image.tag -}}
"{{ .Values.image.repository }}:{{ .Values.image.tag }}"
{{- else -}}
"{{ .Values.image.repository }}{{ .Values.image.default }}"
{{- end -}}
{{- end -}}



{{/*
Create the name of the service account to use
*/}}
{{- define "kitlogin.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{ default (include "kitlogin.fullname" .) .Values.serviceAccount.name }}
{{- else -}}
    {{ default "default" .Values.serviceAccount.name }}
{{- end -}}
{{- end -}}

{{- define "kitlogin.helmOperation" -}}
{{- if .Release.IsUpgrade -}}
    upgrade
{{- else -}}
    install
{{- end -}}
{{- end -}}

{{- define "ingress.type" -}}
{{- if ne (.Values.ingress.type | toString) "<nil>" -}}
  {{ .Values.ingress.type }}
{{- else if .Values.ingress.nginx.enabled -}}
  nginx
{{- else if (eq (.Values.cloud | toString) "gcp") -}}
  clb
{{- end -}}
{{- end -}}


{{- define "kitlogin.helmInstallInfo" -}}
{{- $info := dict }}
{{- $info := set $info "cloud" (required "'cloud' value is required, e.g. 'gcp', 'aws', 'do', 'private', ..." .Values.cloud) -}}
{{- $info := set $info "chart_version" .Chart.Version -}}
{{- $info := set $info "release_name" .Release.Name -}}
{{- $info := set $info "release_revision" .Release.Revision -}}
{{- $info := set $info "hostname" .Values.ingress.hostname -}}
{{- $info := set $info "operation" (include "kitlogin.helmOperation" .) -}}
{{- $info := set $info "ingress_type" (include "ingress.type" .) -}}
{{- $info := set $info "deployment_type" (.Values.deploymentType | default "helm") -}}
{{- $info := set $info "kube_version" .Capabilities.KubeVersion.Version -}}
{{ toJson $info | quote }}
{{- end -}}

{{- define "kitlogin.deploymentEnv" -}}
    helm_{{ .Values.cloud }}_ha
{{- end -}}

{{- define "ingress.letsencrypt" -}}
{{- if ne (.Values.ingress.letsencrypt | toString) "<nil>" -}}
  {{ .Values.ingress.letsencrypt }}
{{- else if and (and (.Values.ingress.nginx.enabled) ( index .Values "cert-manager" "enabled" )) (ne (.Values.ingress.hostname | toString) "<nil>")  -}}
  true
{{- else -}}
  false
{{- end -}}
{{- end -}}
