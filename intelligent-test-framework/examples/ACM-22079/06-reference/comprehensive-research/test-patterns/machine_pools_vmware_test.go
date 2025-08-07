package machine_pools

import (
	"fmt"

	"github.com/onsi/ginkgo/v2"
	libgoclusters "github.com/stolostron/acmqe-go-library/pkg/clusters"
)

var _ = ginkgo.Describe("VMWare Machine Pools", ginkgo.Label("machinepools"), func() {
	ginkgo.BeforeEach(func() {
		var cloudProvider = "vsphere"
		_, err := libgoclusters.GetHiveClusterNamespaces(Appliers, cloudProvider)
		if err != nil {
			ginkgo.Skip(fmt.Sprintf("Skipping test due to failure in GetHiveClusterNamespaces: %v", err))
		}
	})

	// Scale Up
	ginkgo.It("RHACM4K-24027 - As a cluster-admin with an ACM-created VMware cluster, I want to scale up machine pools", ginkgo.Label("RHACM4K-24027", "scale", "vmware"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "vsphere", false, 1, 0, 0, "", "")
	})

	// Scale Down
	ginkgo.It("RHACM4K-24033 - As a cluster-admin with an ACM-created VMware cluster, I want to scale down my machine pools", ginkgo.Label("RHACM4K-24033", "scale", "vmware"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "vsphere", false, -1, 0, 0, "", "")
	})

	// Autoscale Up
	ginkgo.It("RHACM4K-24040 - As a cluster-admin with an ACM-created VMware cluster, I want to autoscale up my machine pools", ginkgo.Label("RHACM4K-24040", "autoscale", "vmware"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "vsphere", true, 0, 1, 1, "", "")
	})

	// Autoscale Down
	ginkgo.It("RHACM4K-24045 - As a cluster-admin with an ACM-created VMware cluster, I want to autoscale down my machine pools", ginkgo.Label("RHACM4K-24045", "autoscale", "vmware"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "vsphere", true, 0, -1, -1, "", "")
	})
})
