package machine_pools

import (
	"fmt"

	"github.com/onsi/ginkgo/v2"
	libgoclusters "github.com/stolostron/acmqe-go-library/pkg/clusters"
)

var _ = ginkgo.Describe("OopenStack Machine Pools", ginkgo.Label("machinepools"), func() {
	ginkgo.BeforeEach(func() {
		var cloudProvider = "openstack"
		_, err := libgoclusters.GetHiveClusterNamespaces(Appliers, cloudProvider)
		if err != nil {
			ginkgo.Skip(fmt.Sprintf("Skipping test due to failure in GetHiveClusterNamespaces: %v", err))
		}
	})

	// Scale Up
	ginkgo.It("RHACM4K-24029 - As a cluster-admin with an ACM-created OpenStack cluster, I want to scale up machine pools", ginkgo.Label("RHACM4K-24029", "scale", "openstack"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "openstack", false, 1, 0, 0, "", "")
	})

	// Scale Down
	ginkgo.It("RHACM4K-24035 - As a cluster-admin with an ACM-created OpenStack cluster, I want to scale down my machine pools", ginkgo.Label("RHACM4K-24035", "scale", "openstack"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "openstack", false, -1, 0, 0, "", "")
	})

	// Autoscale Up
	ginkgo.It("RHACM4K-24042 - As a cluster-admin with an ACM-created OpenStack cluster, I want to autoscale up my machine pools", ginkgo.Label("RHACM4K-24042", "autoscale", "openstack"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "openstack", true, 0, 1, 1, "", "")
	})

	// Autoscale Down
	ginkgo.It("RHACM4K-24047 - As a cluster-admin with an ACM-created OpenStack cluster, I want to autoscale down my machine pools", ginkgo.Label("RHACM4K-24047", "autoscale", "openstack"), func() {
		libgoclusters.MachinePoolScalingCheck(Appliers, "openstack", true, 0, -1, -1, "", "")
	})
})
