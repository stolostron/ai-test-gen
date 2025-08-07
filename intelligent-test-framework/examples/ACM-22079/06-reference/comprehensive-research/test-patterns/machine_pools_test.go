package machine_pools_test

import (
	"github.com/onsi/ginkgo/v2"
	libgoclusters "github.com/stolostron/acmqe-go-library/pkg/clusters"
)

var _ = ginkgo.Describe("machine pools", ginkgo.Label("machinepools"), func() {
	// Scale Up
	ginkgo.It("RHACM4K-24024 - As a cluster-admin with an ACM-created AWS cluster, I want to scale up machine pools", ginkgo.Label("RHACM4K-24024", "scale", "aws"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "aws", false, 1, 0, 0, "", "")
	})

	ginkgo.It("RHACM4K-24025 - As a cluster-admin with an ACM-created GCP cluster, I want to scale up machine pools", ginkgo.Label("RHACM4K-24025", "scale", "gcp"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "gcp", false, 1, 0, 0, "", "")
	})

	ginkgo.It("RHACM4K-24026 - As a cluster-admin with an ACM-created Azure cluster, I want to scale up machine pools", ginkgo.Label("RHACM4K-24026", "scale", "azure"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "azure", false, 1, 0, 0, "", "")
	})

	ginkgo.It("RHACM4K-24027 - As a cluster-admin with an ACM-created VMware cluster, I want to scale up machine pools", ginkgo.Label("RHACM4K-24027", "scale", "vmware"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "vsphere", false, 1, 0, 0, "", "")
	})

	// ginkgo.It("RHACM4K-24029 - As a cluster-admin with an ACM-created OpenStack cluster, I want to scale up machine pools", ginkgo.Label("RHACM4K-24029", "scale", "openstack"), func() {
	// 	MachinePoolScalingCheck(Appliers, "openstack", false, 1, 0, 0, "", "")
	// })

	// Scale Down
	ginkgo.It("RHACM4K-24030 - As a cluster-admin with an ACM-created AWS cluster, I want to scale down my machine pools", ginkgo.Label("RHACM4K-24030", "scale", "aws"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "aws", false, -1, 0, 0, "", "")
	})

	ginkgo.It("RHACM4K-24031 - As a cluster-admin with an ACM-created GCP cluster, I want to scale down my machine pools", ginkgo.Label("RHACM4K-24031", "scale", "gcp"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "gcp", false, -1, 0, 0, "", "")
	})

	ginkgo.It("RHACM4K-24032 - As a cluster-admin with an ACM-created Azure cluster, I want to scale down my machine pools", ginkgo.Label("RHACM4K-24032", "scale", "azure"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "azure", false, -1, 0, 0, "", "")
	})

	ginkgo.It("RHACM4K-24033 - As a cluster-admin with an ACM-created VMware cluster, I want to scale down my machine pools", ginkgo.Label("RHACM4K-24033", "scale", "vmware"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "vsphere", false, -1, 0, 0, "", "")
	})

	// ginkgo.It("RHACM4K-24035 - As a cluster-admin with an ACM-created OpenStack cluster, I want to scale down my machine pools", ginkgo.Label("RHACM4K-24035", "scale", "openstack"), func() {
	// 	MachinePoolScalingCheck(Appliers, "openstack", false, -1, 0, 0)
	// })

	// Autoscale Up
	ginkgo.It("RHACM4K-24036 - As a cluster-admin with an ACM-created AWS cluster, I want to autoscale up my machine pools", ginkgo.Label("RHACM4K-24036", "autoscale", "aws"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "aws", true, 0, 1, 1, "", "")
	})

	ginkgo.It("RHACM4K-24038 - As a cluster-admin with an ACM-created GCP cluster, I want to autoscale up my machine pools", ginkgo.Label("RHACM4K-24038", "autoscale", "gcp"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "gcp", true, 0, 1, 1, "", "")
	})

	ginkgo.It("RHACM4K-24039 - As a cluster-admin with an ACM-created Azure cluster, I want to autoscale up my machine pools", ginkgo.Label("RHACM4K-24039", "autoscale", "azure"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "azure", true, 0, 1, 1, "", "")
	})

	ginkgo.It("RHACM4K-24040 - As a cluster-admin with an ACM-created VMware cluster, I want to autoscale up my machine pools", ginkgo.Label("RHACM4K-24040", "autoscale", "vmware"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "vsphere", true, 0, 1, 1, "", "")
	})

	// ginkgo.It("RHACM4K-24042 - As a cluster-admin with an ACM-created OpenStack cluster, I want to autoscale up my machine pools", ginkgo.Label("RHACM4K-24042", "autoscale", "openstack"), func() {
	// 	MachinePoolScalingCheck(Appliers, "openstack", true, 0, 1, 1)
	// })

	// Autoscale Down
	ginkgo.It("RHACM4K-24048 - As a cluster-admin with an ACM-created AWS cluster, I want to autoscale down my machine pools", ginkgo.Label("RHACM4K-24048", "autoscale", "aws"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "aws", true, 0, -1, -1, "", "")
	})

	ginkgo.It("RHACM4K-24043 - As a cluster-admin with an ACM-created GCP cluster, I want to autoscale down my machine pools", ginkgo.Label("RHACM4K-24043", "autoscale", "gcp"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "gcp", true, 0, -1, -1, "", "")
	})

	ginkgo.It("RHACM4K-24044 - As a cluster-admin with an ACM-created Azure cluster, I want to autoscale down my machine pools", ginkgo.Label("RHACM4K-24044", "autoscale", "azure"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "azure", true, 0, -1, -1, "", "")
	})

	ginkgo.It("RHACM4K-24045 - As a cluster-admin with an ACM-created VMware cluster, I want to autoscale down my machine pools", ginkgo.Label("RHACM4K-24045", "autoscale", "vmware"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "vsphere", true, 0, -1, -1, "", "")
	})

	// ginkgo.It("RHACM4K-24047 - As a cluster-admin with an ACM-created OpenStack cluster, I want to autoscale down my machine pools", ginkgo.Label("RHACM4K-24047", "autoscale", "openstack"), func() {
	// 	MachinePoolScalingCheck(Appliers, "openstack", true, 0, -1, -1, "", "")
	// })
})
