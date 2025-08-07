package destroy_cluster

import (
	"context"

	"github.com/onsi/ginkgo/v2"
	"github.com/onsi/gomega"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

var _ = ginkgo.Describe("detach clusters", ginkgo.Label("detach"), func() {

	ginkgo.It("RHACM4K-46726: CLC: Detach IKS cluster via ManagedCluster", ginkgo.Label("iks"), func() {
		mcs, err := Appliers.ClusterClient.ClusterV1().ManagedClusters().List(context.TODO(), metav1.ListOptions{LabelSelector: "vendor=IKS,cloud=IBM,name!=local-cluster,owner=acmqe-clc-auto"})
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		for _, mc := range mcs.Items {
			err := Appliers.DestroyCluster(mc.Name)
			gomega.Expect(err).NotTo(gomega.HaveOccurred())
		}
	})

	ginkgo.It("RHACM4K-46725: CLC: Detach EKS cluster via ManagedCluster", ginkgo.Label("eks"), func() {
		mcs, err := Appliers.ClusterClient.ClusterV1().ManagedClusters().List(context.TODO(), metav1.ListOptions{LabelSelector: "vendor=EKS,cloud=Amazon,name!=local-cluster,owner=acmqe-clc-auto"})
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		for _, mc := range mcs.Items {
			err := Appliers.DestroyCluster(mc.Name)
			gomega.Expect(err).NotTo(gomega.HaveOccurred())
		}
	})

	ginkgo.It("RHACM4K-46727: CLC: Detach GKE cluster via ManagedCluster", ginkgo.Label("gke"), func() {
		mcs, err := Appliers.ClusterClient.ClusterV1().ManagedClusters().List(context.TODO(), metav1.ListOptions{LabelSelector: "vendor=GKE,cloud=Google,name!=local-cluster,owner=acmqe-clc-auto"})
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		for _, mc := range mcs.Items {
			err := Appliers.DestroyCluster(mc.Name)
			gomega.Expect(err).NotTo(gomega.HaveOccurred())
		}
	})

	ginkgo.It("RHACM4K-46730: CLC: Detach ROKS cluster via ManagedCluster", ginkgo.Label("roks"), func() {
		mcs, err := Appliers.ClusterClient.ClusterV1().ManagedClusters().List(context.TODO(), metav1.ListOptions{LabelSelector: "vendor=OpenShift,cloud=IBM,name!=local-cluster,owner=acmqe-clc-auto"})
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		for _, mc := range mcs.Items {
			err := Appliers.DestroyCluster(mc.Name)
			gomega.Expect(err).NotTo(gomega.HaveOccurred())
		}
	})

	ginkgo.It("RHACM4K-46729: CLC: Detach OCP3 cluster via ManagedCluster", ginkgo.Label("ocp311"), func() {
		mcs, err := Appliers.ClusterClient.ClusterV1().ManagedClusters().List(context.TODO(), metav1.ListOptions{LabelSelector: "vendor=OpenShift,openshiftVersion=3,owner=acmqe-clc-auto"})
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		for _, mc := range mcs.Items {
			err := Appliers.DestroyCluster(mc.Name)
			gomega.Expect(err).NotTo(gomega.HaveOccurred())
		}
	})

	ginkgo.It("RHACM4K-46731: CLC: Detach ROSA HCP cluster via ManagedCluster", ginkgo.Label("rosa-hcp"), func() {
		mcs, err := Appliers.ClusterClient.ClusterV1().ManagedClusters().List(context.TODO(), metav1.ListOptions{LabelSelector: "vendor=OpenShift,cloud=Amazon,name!=local-cluster,owner=acmqe-clc-auto"})
		gomega.Expect(err).ShouldNot(gomega.HaveOccurred())
		for _, mc := range mcs.Items {
			err := Appliers.DestroyCluster(mc.Name)
			gomega.Expect(err).NotTo(gomega.HaveOccurred())
		}
	})
})
